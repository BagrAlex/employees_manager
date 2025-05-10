from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional

class EmployeeForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%m-%d', validators=[DataRequired()])
    personal_number = StringField('Personal Number', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    workplace = StringField('Workplace', validators=[DataRequired()])
    contract_start_date = DateField('Contract Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    contacts = StringField('Contacts', validators=[Optional()])
    photo = FileField('Photo', validators=[Optional()])
    submit = SubmitField('Save')

class PositionDurationForm(FlaskForm):
    position = StringField('Position', validators=[DataRequired()])
    duration_months = IntegerField('Duration (months)', validators=[DataRequired()])
    submit = SubmitField('Save')
    
class SystemSettingsForm(FlaskForm):
    registration_enabled = BooleanField('Enable Registration', default=True)
    submit = SubmitField('Save Settings')

class EmployeeFieldForm(FlaskForm):
    name = StringField('Field Name', validators=[DataRequired()])
    field_type = SelectField('Field Type', choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Field')

class EmployeeFieldValueForm(FlaskForm):
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Save Value')