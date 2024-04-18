from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class ProjectStatusUpdateForm(FlaskForm):
    status_choices = [('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')]
    
    status = SelectField("Status", choices=status_choices, validators=[DataRequired()])
    
    submit = SubmitField('Submit')