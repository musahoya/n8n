"""
Flask 기반 멀티 에이전트 워크플로우 웹 애플리케이션
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from agents.planner_agent import PlannerAgentMultiModel, TopicSuggestion
from agents.writer_agent import WriterAgentMultiModel
from agents.reviewer_agent import ReviewerAgentMultiModel
from agents.image_prompt_agent import ImagePromptAgent
from agents.publisher_agent import PublisherAgent

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """허용된 파일 확장자인지 확인"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """홈페이지 - API 키 및 모델 선택"""
    return render_template('index.html')


@app.route('/setup', methods=['POST'])
def setup():
    """API 키 및 모델 설정 저장"""
    # API 키 저장
    session['gemini_api_key'] = request.form.get('gemini_api_key', '').strip()
    session['claude_api_key'] = request.form.get('claude_api_key', '').strip()
    session['openai_api_key'] = request.form.get('openai_api_key', '').strip()

    # 모델 선택 저장
    session['planner_model'] = request.form.get('planner_model', 'gemini')
    session['writer_model'] = request.form.get('writer_model', 'claude')
    session['reviewer_model'] = request.form.get('reviewer_model', 'gpt')

    # 퍼블리싱 설정 (선택)
    session['naver_client_id'] = request.form.get('naver_client_id', '').strip()
    session['naver_client_secret'] = request.form.get('naver_client_secret', '').strip()
    session['naver_blog_id'] = request.form.get('naver_blog_id', '').strip()
    session['google_api_key'] = request.form.get('google_api_key', '').strip()
    session['google_blog_id'] = request.form.get('google_blog_id', '').strip()
    session['google_access_token'] = request.form.get('google_access_token', '').strip()

    flash('설정이 저장되었습니다!', 'success')
    return redirect(url_for('step1_business_type'))


@app.route('/step1')
def step1_business_type():
    """Step 1: 업종 입력"""
    if 'gemini_api_key' not in session and 'claude_api_key' not in session:
        flash('먼저 API 키를 설정해주세요.', 'warning')
        return redirect(url_for('index'))

    return render_template('step1_business_type.html')


@app.route('/step2', methods=['POST'])
def step2_topic_planning():
    """Step 2: 주제 기획"""
    business_type = request.form.get('business_type', '').strip()

    if not business_type:
        flash('업종을 입력해주세요.', 'error')
        return redirect(url_for('step1_business_type'))

    session['business_type'] = business_type

    try:
        # Agent 1: 주제 기획
        planner = PlannerAgentMultiModel(
            model_type=session['planner_model'],
            gemini_api_key=session.get('gemini_api_key'),
            claude_api_key=session.get('claude_api_key'),
            openai_api_key=session.get('openai_api_key')
        )

        topics = planner.suggest_topics(business_type)
        session['topics'] = [t.to_dict() for t in topics]

        return render_template(
            'step2_topic_selection.html',
            business_type=business_type,
            topics=topics,
            planner_model=session['planner_model']
        )

    except Exception as e:
        flash(f'오류 발생: {str(e)}', 'error')
        return redirect(url_for('step1_business_type'))


@app.route('/step3', methods=['POST'])
def step3_content_writing():
    """Step 3: 콘텐츠 작성"""
    topic_index = int(request.form.get('topic_index', 0))
    topics = session.get('topics', [])

    if topic_index >= len(topics):
        flash('잘못된 주제 선택입니다.', 'error')
        return redirect(url_for('step1_business_type'))

    selected_topic = topics[topic_index]
    session['selected_topic'] = selected_topic

    try:
        # Agent 2: 콘텐츠 작성
        writer = WriterAgentMultiModel(
            model_type=session['writer_model'],
            gemini_api_key=session.get('gemini_api_key'),
            claude_api_key=session.get('claude_api_key'),
            openai_api_key=session.get('openai_api_key')
        )

        contents = writer.write_content(
            topic_keyword=selected_topic['keyword'],
            topic_title=selected_topic['title'],
            topic_reason=selected_topic['reason'],
            business_type=session['business_type']
        )

        session['contents'] = [c.to_dict() for c in contents]

        return render_template(
            'step3_content_display.html',
            topic=selected_topic,
            contents=contents,
            writer_model=session['writer_model']
        )

    except Exception as e:
        flash(f'오류 발생: {str(e)}', 'error')
        return redirect(url_for('step1_business_type'))


@app.route('/step4', methods=['POST'])
def step4_content_review():
    """Step 4: 콘텐츠 검수"""
    platform = request.form.get('platform', 'naver')
    contents = session.get('contents', [])

    # 선택한 플랫폼의 콘텐츠 찾기
    content_obj = next((c for c in contents if c['platform'] == platform), None)

    if not content_obj:
        flash('콘텐츠를 찾을 수 없습니다.', 'error')
        return redirect(url_for('step1_business_type'))

    session['selected_platform'] = platform
    session['selected_content'] = content_obj

    try:
        # Agent 3: 검수
        reviewer = ReviewerAgentMultiModel(
            model_type=session['reviewer_model'],
            gemini_api_key=session.get('gemini_api_key'),
            claude_api_key=session.get('claude_api_key'),
            openai_api_key=session.get('openai_api_key')
        )

        review_result = reviewer.review_content(
            content=content_obj['content'],
            platform=platform,
            business_type=session['business_type']
        )

        session['review_result'] = review_result.to_dict()

        return render_template(
            'step4_review.html',
            platform=platform,
            content=content_obj,
            review=review_result,
            reviewer_model=session['reviewer_model']
        )

    except Exception as e:
        flash(f'오류 발생: {str(e)}', 'error')
        return redirect(url_for('step1_business_type'))


@app.route('/step5')
def step5_image_prompt():
    """Step 5: 이미지 프롬프트 생성 및 업로드"""
    if 'selected_content' not in session:
        flash('먼저 콘텐츠를 생성해주세요.', 'error')
        return redirect(url_for('step1_business_type'))

    try:
        # Agent 4: 이미지 프롬프트 생성
        image_agent = ImagePromptAgent(
            gemini_api_key=session.get('gemini_api_key')
        )

        prompt = image_agent.generate_image_prompt(
            content=session['selected_content']['content'],
            keyword=session['selected_topic']['keyword'],
            platform=session['selected_platform']
        )

        session['image_prompt'] = prompt

        return render_template(
            'step5_image_upload.html',
            prompt=prompt
        )

    except Exception as e:
        flash(f'오류 발생: {str(e)}', 'error')
        return redirect(url_for('step1_business_type'))


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """이미지 업로드 처리"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': '이미지가 없습니다.'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': '파일이 선택되지 않았습니다.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        session['uploaded_image'] = filename

        return jsonify({
            'success': True,
            'filename': filename,
            'url': url_for('static', filename=f'uploads/{filename}')
        })

    return jsonify({'success': False, 'error': '허용되지 않는 파일 형식입니다.'}), 400


@app.route('/step6')
def step6_final_preview():
    """Step 6: 최종 미리보기"""
    if 'selected_content' not in session:
        flash('먼저 콘텐츠를 생성해주세요.', 'error')
        return redirect(url_for('step1_business_type'))

    image_filename = session.get('uploaded_image')
    image_url = url_for('static', filename=f'uploads/{image_filename}') if image_filename else None

    return render_template(
        'step6_preview.html',
        topic=session.get('selected_topic'),
        content=session.get('selected_content'),
        platform=session.get('selected_platform'),
        review=session.get('review_result'),
        image_url=image_url,
        image_prompt=session.get('image_prompt')
    )


@app.route('/publish', methods=['POST'])
def publish():
    """최종 퍼블리싱"""
    if 'selected_content' not in session:
        flash('먼저 콘텐츠를 생성해주세요.', 'error')
        return redirect(url_for('step1_business_type'))

    try:
        # 퍼블리싱 설정
        naver_config = None
        google_config = None

        if session.get('naver_client_id'):
            naver_config = {
                'client_id': session['naver_client_id'],
                'client_secret': session['naver_client_secret'],
                'blog_id': session['naver_blog_id']
            }

        if session.get('google_api_key') and session.get('google_blog_id'):
            google_config = {
                'api_key': session['google_api_key'],
                'blog_id': session['google_blog_id'],
                'access_token': session.get('google_access_token')
            }

        publisher = PublisherAgent(
            naver_config=naver_config,
            google_config=google_config
        )

        # 이미지 경로
        image_path = None
        if session.get('uploaded_image'):
            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                session['uploaded_image']
            )

        # 퍼블리싱 실행
        platform = session['selected_platform']
        title = session['selected_topic']['title']
        content = session['selected_content']['content']

        if platform == 'naver':
            result = publisher.publish_to_naver(title, content, image_path)
        elif platform == 'google':
            result = publisher.publish_to_google(title, content, image_path)
        else:
            flash('지원하지 않는 플랫폼입니다.', 'error')
            return redirect(url_for('step6_final_preview'))

        return render_template(
            'publish_result.html',
            platform=platform,
            result=result
        )

    except Exception as e:
        flash(f'퍼블리싱 오류: {str(e)}', 'error')
        return redirect(url_for('step6_final_preview'))


@app.route('/reset')
def reset():
    """세션 초기화"""
    session.clear()
    flash('세션이 초기화되었습니다.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
