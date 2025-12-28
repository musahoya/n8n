"""
Flask 기반 멀티 에이전트 블로그 자동화 시스템
단계별로 명확하게 진행됩니다.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
from multi_model_agent import MultiModelAgent
from agents.planner_agent import PlannerAgentMultiModel
from agents.writer_agent import WriterAgentMultiModel
from agents.reviewer_agent import ReviewerAgentMultiModel
from agents.image_prompt_agent import ImagePromptAgent

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 세션 암호화 (창 닫으면 사라짐)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """시작 페이지 - API 키 입력"""
    return render_template('index.html')


@app.route('/setup', methods=['POST'])
def setup():
    """API 키를 세션에 저장 (창 닫으면 사라짐)"""
    # API 키 저장
    session['gemini_key'] = request.form.get('gemini_key', '').strip()
    session['claude_key'] = request.form.get('claude_key', '').strip()
    session['openai_key'] = request.form.get('openai_key', '').strip()

    # 모델 선택 저장
    session['model1'] = request.form.get('model1', 'gemini')  # 주제 생성
    session['model2'] = request.form.get('model2', 'gemini')  # 콘텐츠 작성
    session['model3'] = request.form.get('model3', 'gemini')  # 리뷰

    # 세션 초기화
    session.pop('topics', None)
    session.pop('contents', None)
    session.pop('review', None)

    return redirect(url_for('step1'))


@app.route('/step1')
def step1():
    """1단계: 비즈니스 유형 입력"""
    return render_template('step1.html')


@app.route('/step1_process', methods=['POST'])
def step1_process():
    """1단계 처리: 주제 생성"""
    business = request.form.get('business', '').strip()

    if not business:
        flash('비즈니스 유형을 입력하세요')
        return redirect(url_for('step1'))

    try:
        # 주제 생성 에이전트
        planner = PlannerAgentMultiModel(
            model_type=session.get('model1', 'gemini'),
            gemini_api_key=session.get('gemini_key'),
            claude_api_key=session.get('claude_key'),
            openai_api_key=session.get('openai_key')
        )

        topics = planner.suggest_topics(business)

        # 세션에 저장
        session['business'] = business
        session['topics'] = [
            {'keyword': t.keyword, 'title': t.title, 'reason': t.reason}
            for t in topics
        ]

        # 2단계로 이동
        return redirect(url_for('step2'))

    except Exception as e:
        flash(f'오류: {str(e)}')
        return redirect(url_for('step1'))


@app.route('/step2')
def step2():
    """2단계: 주제 선택"""
    if 'topics' not in session:
        flash('먼저 1단계를 완료하세요')
        return redirect(url_for('step1'))

    return render_template('step2.html', topics=session['topics'])


@app.route('/step2_process', methods=['POST'])
def step2_process():
    """2단계 처리: 콘텐츠 작성"""
    idx = int(request.form.get('topic_idx', 0))

    if idx >= len(session.get('topics', [])):
        flash('잘못된 선택')
        return redirect(url_for('step2'))

    try:
        topic = session['topics'][idx]

        # 콘텐츠 작성 에이전트
        writer = WriterAgentMultiModel(
            model_type=session.get('model2', 'gemini'),
            gemini_api_key=session.get('gemini_key'),
            claude_api_key=session.get('claude_key'),
            openai_api_key=session.get('openai_key')
        )

        contents = writer.write_content(
            topic_keyword=topic['keyword'],
            topic_title=topic['title'],
            topic_reason=topic['reason'],
            business_type=session['business']
        )

        # 세션에 저장
        session['selected_topic'] = topic
        session['contents'] = [
            {'platform': c.platform, 'title': c.title, 'content': c.content}
            for c in contents
        ]

        # 3단계로 이동
        return redirect(url_for('step3'))

    except Exception as e:
        flash(f'오류: {str(e)}')
        return redirect(url_for('step2'))


@app.route('/step3')
def step3():
    """3단계: 콘텐츠 선택"""
    if 'contents' not in session:
        flash('먼저 2단계를 완료하세요')
        return redirect(url_for('step2'))

    return render_template('step3.html', contents=session['contents'])


@app.route('/step3_process', methods=['POST'])
def step3_process():
    """3단계 처리: 리뷰"""
    idx = int(request.form.get('content_idx', 0))

    if idx >= len(session.get('contents', [])):
        flash('잘못된 선택')
        return redirect(url_for('step3'))

    try:
        content = session['contents'][idx]

        # 리뷰 에이전트
        reviewer = ReviewerAgentMultiModel(
            model_type=session.get('model3', 'gemini'),
            gemini_api_key=session.get('gemini_key'),
            claude_api_key=session.get('claude_key'),
            openai_api_key=session.get('openai_key')
        )

        review = reviewer.review_content(
            title=content['title'],
            content=content['content'],
            platform=content['platform']
        )

        # 세션에 저장
        session['selected_content'] = content
        session['review'] = {
            'score': review.score,
            'approved': review.approved,
            'suggestions': review.suggestions
        }

        # 4단계로 이동
        return redirect(url_for('step4'))

    except Exception as e:
        flash(f'오류: {str(e)}')
        return redirect(url_for('step3'))


@app.route('/step4')
def step4():
    """4단계: 이미지 프롬프트 및 업로드"""
    if 'review' not in session:
        flash('먼저 3단계를 완료하세요')
        return redirect(url_for('step3'))

    # 이미지 프롬프트 자동 생성
    try:
        if 'image_prompt' not in session:
            img_agent = ImagePromptAgent(
                gemini_api_key=session.get('gemini_key')
            )

            prompt_result = img_agent.generate_image_prompt(
                topic_title=session['selected_topic']['title'],
                content=session['selected_content']['content']
            )

            session['image_prompt'] = prompt_result.english_prompt
    except:
        session['image_prompt'] = '이미지 프롬프트를 생성할 수 없습니다.'

    return render_template('step4.html',
                         prompt=session.get('image_prompt'),
                         review=session.get('review'))


@app.route('/step4_upload', methods=['POST'])
def step4_upload():
    """4단계: 이미지 업로드"""
    if 'image' not in request.files:
        flash('이미지를 선택하세요')
        return redirect(url_for('step4'))

    file = request.files['image']

    if file.filename == '':
        flash('파일을 선택하세요')
        return redirect(url_for('step4'))

    # 파일 저장
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    session['image'] = filename

    # 5단계로 이동
    return redirect(url_for('step5'))


@app.route('/step5')
def step5():
    """5단계: 발행 완료"""
    if 'image' not in session:
        flash('먼저 4단계를 완료하세요')
        return redirect(url_for('step4'))

    return render_template('step5.html',
                         topic=session.get('selected_topic'),
                         content=session.get('selected_content'),
                         review=session.get('review'),
                         image=session.get('image'))


@app.route('/reset')
def reset():
    """처음부터 다시 시작"""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Flask 서버 시작")
    print("="*60)
    print("브라우저에서 http://localhost:5000 접속하세요")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
