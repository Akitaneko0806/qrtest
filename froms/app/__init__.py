import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
session = Session()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    session.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    configure_logging(app)
    configure_error_handlers(app)
    log_configuration(app)

    @app.after_request
    def add_csrf_token_to_response(response):
        response.set_cookie('csrf_token', csrf.generate_csrf())
        return response

    return app

def configure_logging(app):
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Survey startup')

def log_configuration(app):
    app.logger.info("Loaded configuration:")
    app.logger.info(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    app.logger.info(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    app.logger.info(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    app.logger.info(f"MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    app.logger.info(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    app.logger.info(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    app.logger.info(f"WTF_CSRF_SECRET_KEY: {'設定済み' if app.config.get('WTF_CSRF_SECRET_KEY') else '未設定'}")

def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return 'Page not found', 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return 'Internal server error', 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        app.logger.error(f"CSRFエラーが発生しました: {e}")
        return jsonify(error="CSRFトークンが無効です。ページを更新して再度お試しください。"), 400

# アプリケーションインスタンスを作成
app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)