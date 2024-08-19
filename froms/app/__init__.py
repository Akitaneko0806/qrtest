import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
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
    log_configuration(app)

    return app

def configure_logging(app):
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)

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
    app.logger.info(f"Mail configuration: SERVER={app.config.get('MAIL_SERVER')}, "
                    f"PORT={app.config.get('MAIL_PORT')}, "
                    f"USE_TLS={app.config.get('MAIL_USE_TLS')}, "
                    f"USE_SSL={app.config.get('MAIL_USE_SSL')}")

# CSRFエラーハンドラの追加
@csrf.error_handler
def handle_csrf_error(e):
    return "CSRF検証に失敗しました。ページを更新して再度お試しください。", 400

# アプリケーションインスタンスを作成
app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)