import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # セッション設定
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # メール設定
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # CSRF設定
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'csrf-secret-key'

    @staticmethod
    def init_app(app):
        pass

    @classmethod
    def init_app(cls, app):
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'hard-to-guess-string':
            app.logger.warning('SECRET_KEY is not set or is using default value')
        if not cls.WTF_CSRF_SECRET_KEY or cls.WTF_CSRF_SECRET_KEY == 'csrf-secret-key':
            app.logger.warning('WTF_CSRF_SECRET_KEY is not set or is using default value')