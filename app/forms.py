from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
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
    
    submit = SubmitField('Update')
    
    def validate_first_name(self, first_name):
        if first_name.data != current_user.first_name:
            user = User.query.filter_by(first_name=first_name.data).first()
            if user:
                raise ValidationError('Email already exists in the database')
    
    def validate_last_name(self, last_name):
        if last_name.data != current_user.last_name:
            user = User.query.filter_by(last_name=last_name.data).first()
            if user:
                raise ValidationError('Email already exists in the database')
    
    def validate_depart(self, department):
        if department.data != current_user.department:
            user = User.query.filter_by(department=department.data).first()
            
            if user:
                raise ValidationError('Email already exists in the database')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            
            if user:
                raise ValidationError('Email already exists in the database')
            

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
    
class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Length(min=5, max=100), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email does not exist in the database')
            
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')