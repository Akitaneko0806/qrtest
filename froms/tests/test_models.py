from app.models.survey import Survey
from app.models.user import User
from datetime import datetime

def test_new_survey(app):
    with app.app_context():
        survey = Survey(
            name="New User",
            email="newuser@example.com",
            phone="9876543210",
            postal_code="987-6543",
            address="New Address",
            preferred_date=datetime(2023, 6, 1),
            preferred_location="New Location",
            consent=True
        )
        assert survey.name == "New User"
        assert survey.email == "newuser@example.com"
        assert survey.phone == "9876543210"
        assert survey.postal_code == "987-6543"
        assert survey.address == "New Address"
        assert survey.preferred_date == datetime(2023, 6, 1)
        assert survey.preferred_location == "New Location"
        assert survey.consent == True

def test_survey_to_dict(app, init_database):
    with app.app_context():
        survey = Survey.query.first()
        survey_dict = survey.to_dict()
        
        assert isinstance(survey_dict, dict)
        assert survey_dict['name'] == "Test User"
        assert survey_dict['email'] == "test@example.com"
        assert survey_dict['phone'] == "1234567890"
        assert survey_dict['postal_code'] == "123-4567"
        assert survey_dict['address'] == "Test Address"
        assert "preferred_date" in survey_dict
        assert survey_dict['preferred_location'] == "Test Location"
        assert survey_dict['consent'] == True

def test_new_user(app):
    with app.app_context():
        user = User(username="testuser", email="testuser@example.com")
        user.set_password("password")
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.password_hash != "password"
        assert user.check_password("password")
        assert not user.check_password("wrongpassword")