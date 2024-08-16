import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from config import Config
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    # 設定の読み込みを確認
    print("Loaded configuration:")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    db.init_app(app)
    mail.init_app(app)
    app.config['MAIL_DEBUG'] = True
    migrate.init_app(app, db)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # ロギング設定
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # コンソールにもログを出力
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Survey startup')

    # メール設定のログ
    app.logger.info(f"Mail configuration: SERVER={app.config.get('MAIL_SERVER')}, "
                    f"PORT={app.config.get('MAIL_PORT')}, "
                    f"USE_TLS={app.config.get('MAIL_USE_TLS')}, "
                    f"USE_SSL={app.config.get('MAIL_USE_SSL')}")

    return app

# アプリケーションインスタンスを作成
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)