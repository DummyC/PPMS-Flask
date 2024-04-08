from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = StringField('Department Name', validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=50)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')