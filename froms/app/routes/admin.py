from flask import Blueprint, render_template
from flask_login import login_required
from app.models.survey import Survey

bp = Blueprint('admin', __name__)

@bp.route('/survey_results')
#@login_required
def survey_results():
    surveys = Survey.query.all()
    return render_template('admin/survey_results.html', surveys=surveys)