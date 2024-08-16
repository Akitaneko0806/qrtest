import pytest
from app import create_app, db
from app.models.survey import Survey
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app('testing')
    app.config.from_object(TestingConfig)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        survey = Survey(
            name="Test User",
            email="test@example.com",
            phone="1234567890",
            postal_code="123-4567",
            address="Test Address",
            preferred_date="2023-05-01",
            preferred_location="Test Location",
            consent=True
        )
        db.session.add(survey)
        db.session.commit()
    
    yield db
    
    with app.app_context():
        db.session.remove()
        db.drop_all()