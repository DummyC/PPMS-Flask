from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, DateField, SubmitField, ValidationError
from wtforms.validators import DataRequired
import datetime

def validate_date(form, date_needed):
    if date_needed.data < datetime.date.today():
        raise ValidationError("The date cannot be in the past!")

class ProjectForm(FlaskForm):
    mode_choices = [('Competitive Bidding', 'Competitive Bidding'), ('Agency-to-Agency', 'Agency-to-Agency'), ('Direct Contracting', 'Direct Contracting'), ('Negotiated Procurement', 'Negotiated Procurement'), ('Shopping', 'Shopping'), ('Small Value Procurement', 'Small Value Procurement')]
    source_choices = [('GAA', 'GAA'), ('STF', 'STF')]
    
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    budget = DecimalField('Estimated Budget', validators=[DataRequired()])
    initial_mode = SelectField("Mode of Procurement", choices=mode_choices, validators=[DataRequired()])
    date_needed = DateField('Date Needed', validators=[DataRequired(), validate_date])
    source = SelectField('Source of Fund', choices=source_choices ,validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    
