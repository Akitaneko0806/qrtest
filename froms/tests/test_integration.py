import pytest
from app import create_app, db
from app.models.user import User
from app.models.survey import Survey
from flask_login import login_user
from datetime import datetime

@pytest.fixture
def test_client():
    app = create_app('testing')
    app.config['LOGIN_DISABLED'] = True  # テスト中は認証を無効化
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_survey_submission_and_admin_view(test_client):
    # アンケートの送信
    response = test_client.post('/', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123-456-7890',
        'postal_code': '123-4567',
        'address': 'Test Address',
        'preferred_date': '2023-05-01',
        'preferred_location': 'Test Location',
        'consent': 'y'
    })
    assert response.status_code == 200
    assert b"Survey submitted successfully" in response.data

    # 管理者ページでの確認
    response = test_client.get('/admin/survey_results')
    assert response.status_code == 200
    assert b"Test User" in response.data
    assert b"test@example.com" in response.data

def test_invalid_survey_submission(test_client):
    # 無効なデータでのアンケート送信
    response = test_client.post('/', data={
        'name': '',
        'email': 'invalid-email',
        'phone': 'not-a-phone'
    })
    assert response.status_code == 400
    
    # エラーメッセージの確認
    error_data = response.get_json()
    assert 'name' in error_data
    assert 'email' in error_data
    assert 'phone' in error_data

def test_survey_flow(test_client):
    # アンケートページの表示
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Survey Form" in response.data

    # アンケートの送信
    response = test_client.post('/', data={
        'name': 'Flow Test User',
        'email': 'flowtest@example.com',
        'phone': '987-654-3210',
        'postal_code': '987-6543',
        'address': 'Flow Test Address',
        'preferred_date': '2023-06-01',
        'preferred_location': 'Flow Test Location',
        'consent': 'y'
    })
    assert response.status_code == 200
    assert b"Survey submitted successfully" in response.data

    # データベースでの確認
    with test_client.application.app_context():
        survey = Survey.query.filter_by(email='flowtest@example.com').first()
        assert survey is not None
        assert survey.name == 'Flow Test User'
        assert survey.phone == '987-654-3210'

    # 管理者ページでの確認
    response = test_client.get('/admin/survey_results')
    assert response.status_code == 200
    assert b"Flow Test User" in response.data
    assert b"flowtest@example.com" in response.data