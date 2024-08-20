from app import db

class SurveyData(db.Model):
    __tablename__ = 'survey_data'
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_name_kana = db.Column(db.String(100), nullable=False)
    selectphoneormail = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120))
    contact_info = db.Column(db.String(20))
    contact_time = db.Column(db.String(100))
    proxy = db.Column(db.String(10), nullable=False)
    proxy_name = db.Column(db.String(100))
    proxy_name_kana = db.Column(db.String(100))
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(5), nullable=False)
    meeting_place = db.Column(db.String(50), nullable=False)
    additional_info = db.Column(db.Text)

    def __repr__(self):
        return f'<SurveyData {self.id}>'