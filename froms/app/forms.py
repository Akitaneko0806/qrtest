from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
import re

class SurveyForm(FlaskForm):
    name = StringField('名前', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    phone = StringField('電話番号', validators=[DataRequired()])
    postal_code = StringField('郵便番号', validators=[DataRequired()])
    address = StringField('住所', validators=[DataRequired()])
    preferred_date = DateField('希望日', validators=[DataRequired()])
    preferred_location = StringField('希望場所', validators=[DataRequired()])
    consent = BooleanField('同意', validators=[DataRequired()])

    def validate_phone(self, field):
        if not re.match(r'^\d{2,4}-?\d{2,4}-?\d{3,4}$', field.data):
            raise ValidationError('Invalid phone number format.')

    def validate_postal_code(self, field):
        if not re.match(r'^\d{3}-?\d{4}$', field.data):
            raise ValidationError('Invalid postal code format.')