from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
        
    if user:
        raise ValidationError('Email already exists in the database')

class ProjectStatusUpdateForm(FlaskForm):
    status_choices = [('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')]
    
    status = SelectField("Status", choices=status_choices, validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    
class CreateUserForm(FlaskForm):
    role_choices = [('Head', 'Head'), ('Administrator', 'Administrator')]
    department_choices = [('None', 'None'), ('CBM', 'College of Business Management'), ('CTE', 'College of Teacher Education'), ('CFMS', 'College of Fisheries and Marine Sciences'), ('CoS', 'College of Sciences')]
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = SelectField('Department Name', choices=department_choices ,validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email(), validate_email])
    
    role = SelectField('Role', choices=role_choices, validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')
    
        
class UpdateUserForm(FlaskForm):
    role_choices = [('Head', 'Head'), ('Administrator', 'Administrator')]
    department_choices = [('None', 'None'), ('CBM', 'College of Business Management'), ('CTE', 'College of Teacher Education'), ('CFMS', 'College of Fisheries and Marine Sciences'), ('CoS', 'College of Sciences')]
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = SelectField('Department Name', choices=department_choices, validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    role = SelectField('Role', choices=role_choices, validators=[DataRequired()])
    
    submit = SubmitField('Update')
    