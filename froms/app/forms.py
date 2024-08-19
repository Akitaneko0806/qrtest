from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
import re

class SurveyForm(FlaskForm):
    owner_name = StringField('地権者名', validators=[DataRequired()])
    owner_name_kana = StringField('（ヒラガナ）', validators=[DataRequired()])
    selectphoneormail = SelectField('連絡先選択', choices=[('mail', 'メールアドレス'), ('phone', '携帯番号')], validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[Optional(), Email()])
    contact_info = StringField('お電話番号', validators=[Optional()])
    contact_time = SelectField('電話連絡可能な時間', choices=[
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00')
    ], validators=[Optional()])
    proxy = SelectField('委任の有無', choices=[('あり', 'あり'), ('なし', 'なし')], validators=[DataRequired()])
    proxy_name = StringField('委任者名', validators=[Optional()])
    proxy_name_kana = StringField('（ヒラガナ）', validators=[Optional()])
    preferred_date = DateField('変更希望日時', validators=[DataRequired()])
    preferred_time = SelectField('時間', choices=[
        ('09:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00')
    ], validators=[DataRequired()])
    meeting_place = SelectField('待合せ希望場所', choices=[('自宅', '自宅'), ('〇〇集合', '〇〇集合'), ('その他', 'その他')], validators=[DataRequired()])
    additional_info = TextAreaField('その他', validators=[Optional()])

    def validate_contact_info(self, field):
        if self.selectphoneormail.data == 'phone' and not field.data:
            raise ValidationError('電話番号を入力してください。')
        if field.data and not re.match(r'^\d{2,4}-?\d{2,4}-?\d{3,4}$', field.data):
            raise ValidationError('無効な電話番号の形式です。')

    def validate_email(self, field):
        if self.selectphoneormail.data == 'mail' and not field.data:
            raise ValidationError('メールアドレスを入力してください。')

    def validate_proxy_name(self, field):
        if self.proxy.data == 'あり' and not field.data:
            raise ValidationError('委任者名を入力してください。')

    def validate_proxy_name_kana(self, field):
        if self.proxy.data == 'あり' and not field.data:
            raise ValidationError('委任者名（ヒラガナ）を入力してください。')