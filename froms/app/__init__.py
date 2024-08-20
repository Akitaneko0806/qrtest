from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_session import Session
import logging
from logging.handlers import RotatingFileHandler
from config import Config
import os

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

def configure_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return 'Page not found', 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return 'Internal server error', 500

    from flask_wtf.csrf import CSRFError
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return "CSRF検証に失敗しました。ページを更新して再度お試しください。", 400