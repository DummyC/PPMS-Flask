from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = StringField('Department Name', validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if user:
            raise ValidationError('Email already exists in the database')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=50)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    
class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    department = StringField('Department Name', validators=[DataRequired(), Length(min=5, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Update')
    
    

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            
            if user:
                raise ValidationError('Email already exists in the database')
            
class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
            
    submit = SubmitField('Update')
    
class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email does not exist in the database')
            
class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')