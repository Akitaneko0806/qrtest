import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'your_prefix_'
    # メール設定
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.simmon.jp')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # CSRFの設定
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', SECRET_KEY)

    @classmethod
    def init_app(cls, app):
        # アプリケーション初期化時に追加の設定を行う
        pass

    @classmethod
    def validate_config(cls):
        required_vars = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'MAIL_USERNAME', 'MAIL_PASSWORD']
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"環境変数 {var} が設定されていません。")