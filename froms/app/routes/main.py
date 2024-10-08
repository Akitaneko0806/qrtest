from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.survey import SurveyData
from app import db
from app.services.email_service import send_email
from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf
import logging
from app.forms import SurveyForm

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)
csrf = CSRFProtect()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SurveyForm()
    if form.validate_on_submit():
        return redirect(url_for('main.confirm'))
    return render_template('survey.html', form=form, csrf_token=generate_csrf())

@main_bp.route('/confirm', methods=['POST'])
def confirm():
    form = SurveyForm()
    if form.validate_on_submit():
        survey_data = form.data
        survey_data.pop('csrf_token', None)
        return render_template('confirm.html', survey_data=survey_data, form=form)
    else:
        flash('入力内容に誤りがあります。', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/submit', methods=['POST'])
def submit():
    form = SurveyForm()
    if form.validate_on_submit():
        survey_data = form.data
        survey_data.pop('csrf_token', None)

        new_survey = SurveyData(**survey_data)
        db.session.add(new_survey)
        db.session.commit()

        send_email(to=survey_data['email'], subject='アンケート送信確認', template='thanks_email.html', context=survey_data)
        send_email(to='admin@example.com', subject='新規アンケート送信', template='admin_notification.html', context=survey_data)

        flash('アンケートが正常に送信されました。', 'success')
        return redirect(url_for('main.thanks'))
    else:
        flash('入力内容に誤りがあります。', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/thanks')
def thanks():
    return render_template('thanks.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    logger.error("404エラーが発生しました")
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_server_error(e):
    logger.error("500エラーが発生しました", exc_info=True)
    return render_template('errors/500.html'), 500

@main_bp.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@main_bp.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.error(f"CSRFエラーが発生しました: {e}")
    return jsonify(error="CSRFトークンが無効です。ページを更新してもう一度お試しください。"), 400

@main_bp.after_request
def add_csrf_token_to_response(response):
    response.set_cookie('csrf_token', generate_csrf())
    return response