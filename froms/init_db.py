from app import create_app, db
from app.models.models import SurveyData

app = create_app()

with app.app_context():
    db.create_all()
