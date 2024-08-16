from . import db

class SurveyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(50), nullable=False)
    owner_name_kana = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(20), nullable=True)
    contact_time = db.Column(db.String(100), nullable=True)
    proxy = db.Column(db.String(10), nullable=False)
    proxy_name = db.Column(db.String(50), nullable=True)
    proxy_name_kana = db.Column(db.String(50), nullable=True)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(10), nullable=False)
    meeting_place = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.Text, nullable=True)
