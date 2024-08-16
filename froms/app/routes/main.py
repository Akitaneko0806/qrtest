from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.survey import SurveyData
from app import db
from app.services.email_service import send_email
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    survey_data = request.args.to_dict() if request.method == 'GET' else {}
    return render_template('survey.html', survey_data=survey_data)

@main_bp.route('/confirm', methods=['POST'])
def confirm():
    survey_data = request.form.to_dict()
    return render_template('confirm.html', survey_data=survey_data)

@main_bp.route('/submit', methods=['POST'])
def submit():
    survey_data = request.form.to_dict()
    
    logger.info(f"Submit data: {survey_data}")
    
    try:
        # データベースへの保存
        survey_entry = SurveyData(
            owner_name=survey_data['owner_name'],
            owner_name_kana=survey_data['owner_name_kana'],
            selectphoneormail=survey_data['selectphoneormail'],
            email=survey_data.get('email'),
            contact_info=survey_data.get('contact_info'),
            contact_time=','.join(request.form.getlist('contact_time')),
            proxy=survey_data['proxy'],
            proxy_name=survey_data.get('proxy_name'),
            proxy_name_kana=survey_data.get('proxy_name_kana'),
            preferred_date=survey_data['preferred_date'],
            preferred_time=survey_data['preferred_time'],
            meeting_place=survey_data['meeting_place'],
            additional_info=survey_data.get('additional_info')
        )
        db.session.add(survey_entry)
        db.session.commit()
        logger.info(f"Survey data saved to database. ID: {survey_entry.id}")

        # メールの送信
        send_email(
            to=survey_data['email'],
            subject='アンケート送信確認',
            template='thanks.html',
            context={'survey_data': survey_data}
        )
        logger.info(f"Confirmation email sent to {survey_data['email']}")

        send_email(
            to='admin@example.com',
            subject='アンケート新規送信',
            template='admin/survey_notification.html',
            context={'survey_data': survey_data}
        )
        logger.info("Admin notification email sent")

        flash('アンケートが正常に送信されました。確認メールをご確認ください。', 'success')
        return render_template('thanks.html', survey_data=survey_data)

    except Exception as e:
        logger.error(f"Error occurred during form submission: {str(e)}", exc_info=True)
        db.session.rollback()
        flash('エラーが発生しました。後でもう一度お試しください。', 'error')
        return redirect(url_for('main.index'))

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500