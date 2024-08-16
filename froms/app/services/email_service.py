import smtplib
from email.message import EmailMessage
from flask import current_app, render_template
import logging

logger = logging.getLogger(__name__)

def send_email(to, subject, template, context):
    msg = EmailMessage()
    msg.set_content(render_template(template, **context))
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = to

    try:
        smtp_server = current_app.config['MAIL_SERVER']
        port = current_app.config['MAIL_PORT']
        username = current_app.config['MAIL_USERNAME']
        password = current_app.config['MAIL_PASSWORD']

        logger.debug(f"Attempting to send email to {to} with subject '{subject}'")
        logger.debug(f"SMTP server: {smtp_server}:{port}")
        logger.debug(f"Using TLS: {current_app.config['MAIL_USE_TLS']}, Using SSL: {current_app.config['MAIL_USE_SSL']}")

        with smtplib.SMTP(smtp_server, port) as server:
            server.set_debuglevel(1)  # デバッグ出力を有効化
            if current_app.config['MAIL_USE_TLS']:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {to} with subject '{subject}'")
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {str(e)}", exc_info=True)
        raise

def log_mail_config():
    logger.debug("Mail configuration:")
    logger.debug(f"MAIL_SERVER: {current_app.config['MAIL_SERVER']}")
    logger.debug(f"MAIL_PORT: {current_app.config['MAIL_PORT']}")
    logger.debug(f"MAIL_USE_TLS: {current_app.config['MAIL_USE_TLS']}")
    logger.debug(f"MAIL_USE_SSL: {current_app.config['MAIL_USE_SSL']}")
    logger.debug(f"MAIL_USERNAME: {current_app.config['MAIL_USERNAME']}")