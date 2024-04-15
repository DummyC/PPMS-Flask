from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    mode_choices = [('Competitive Bidding', 'Competitive Bidding'), ('Direct Contracting', 'Direct Contracting'), ('Shopping', 'Shopping'), ('Small Value Procurement', 'Small Value Procurement'), ('Agency-to-Agency', 'Agency-to-Agency'), ('Negotiated Procurement', 'Negotiated Procurement')]
    
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    budget = DecimalField('Estimated Budget', validators=[DataRequired()])
    initial_mode = SelectField("Mode of Procurement", choices=mode_choices, validators=[DataRequired()])
    date_needed = DateField('Date Needed', validators=[DataRequired()])
    source = StringField('Source of Fund', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    
    submit = SubmitField('Submit')