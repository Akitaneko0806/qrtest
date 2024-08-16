from flask import current_app
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import bleach

csrf = CSRFProtect()

def init_app(app):
    csrf.init_app(app)

def encrypt_data(data):
    """データの暗号化"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(data)

def decrypt_data(encrypted_data):
    """データの復号化"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.loads(encrypted_data, max_age=86400)  # 24時間有効

def hash_password(password):
    """パスワードのハッシュ化"""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """パスワードの検証"""
    return check_password_hash(hashed_password, password)

def sanitize_input(input_string):
    """入力値のサニタイズ（XSS対策）"""
    return bleach.clean(input_string)

def validate_input(data, rules):
    """入力値のバリデーション"""
    errors = {}
    for field, rule in rules.items():
        if field not in data:
            errors[field] = "This field is required."
        elif rule == 'email' and '@' not in data[field]:
            errors[field] = "Invalid email format."
        elif rule == 'phone' and not data[field].replace('-', '').isdigit():
            errors[field] = "Invalid phone number format."
    return errors

def db_operation(func):
    """データベース操作のデコレータ（SQLインジェクション対策）"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error: {str(e)}")
            return None
    return wrapper

def record_consent(user_id, consent_type):
    """同意の記録"""
    # ここでデータベースに同意記録を保存する実装を行う
    pass