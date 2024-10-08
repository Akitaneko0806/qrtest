from app import db
from app.models.survey import Survey

def save_survey(survey_data):
    try:
        new_survey = Survey(**survey_data)
        db.session.add(new_survey)
        db.session.commit()
        return new_survey
    except Exception as e:
        db.session.rollback()
        print(f"Error saving survey: {str(e)}")
        return None

def get_survey_by_id(survey_id):
    return Survey.query.get(survey_id)

def get_all_surveys(page=1, per_page=20):
    return Survey.query.order_by(Survey.created_at.desc()).paginate(page=page, per_page=per_page)

def update_survey(survey_id, survey_data):
    survey = Survey.query.get(survey_id)
    if survey:
        for key, value in survey_data.items():
            setattr(survey, key, value)
        db.session.commit()
        return survey
    return None

def delete_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if survey:
        db.session.delete(survey)
        db.session.commit()
        return True
    return False