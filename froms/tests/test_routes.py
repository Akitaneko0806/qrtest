import json
from flask_login import login_user
from app.models.user import User
from app import db
from datetime import datetime

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Survey Form" in response.data

def test_index_post_valid(client):
    response = client.post('/', data={
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

def test_index_post_invalid(client):
    response = client.post('/', data={
        'name': '',
        'email': 'invalid-email',
        'phone': 'not-a-phone'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'name' in data
    assert 'email' in data
    assert 'phone' in data

def test_convert_to_kana(client):
    response = client.post('/api/convert_to_kana', 
                           data=json.dumps({'name': 'Taro Yamada'}),
                           content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['kana'] == 'Taro Yamada'

def test_admin_survey_results(client, app):
    with app.app_context():
        user = User(username='testadmin', email='admin@test.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        with client:
            login_user(user)
            response = client.get('/admin/survey_results')
            assert response.status_code == 200
            assert b"Survey Results" in response.data