from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Project
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, PasswordResetForm, UpdatePasswordForm
from app.users.utils import send_reset_email

users = Blueprint('users', __name__)



@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('projects.projects_list'))
    
    # disable register route if an admin account exists
    
    admin_user = User.query.filter_by(role="Administrator").first()
    if(admin_user):
        return abort(403)
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, department=form.department.data, email=form.email.data, password=hashed_password, role="Administrator")
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('Email already exists', 'danger')
            return redirect(url_for('users.register'))

        
        flash(f'Account created for {form.email.data} successfully, you are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.projects_list'))
    rule = request.url_rule
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif current_user.role == "Administrator":
                return redirect(url_for('admins.admin_dashboard'))
            else:
                return redirect(url_for('projects.projects_list'))
        else:
            flash('Login failed, incorrect email or password', 'danger')
    return render_template('login.html', title='Login', form=form, rule=rule)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('User logged out, please log in', 'info')
    return redirect(url_for('users.login'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
        
        try:
            db.session.commit()
            flash('Account updated successfully', 'success')
        except:
            flash('Error updating account information', 'danger')
            
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@users.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm();
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            new_hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = new_hashed_password
        
        try:
            db.session.commit()
            logout_user()
            flash('Account password updated successfully, please login again', 'success')
            return redirect(url_for('users.login'))
        except:
            flash('Error updating account password', 'danger')
    return render_template('update_password.html', title='Update Password', form=form)
        
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('projects.projects_list'))  
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Password reset email has been sent to your email address', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('projects.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        try:
            db.session.commit()
        except:
            flash('Error resetting password', 'danger')
            return redirect(url_for('users.login'))

        
        flash(f'Password reset for {user.email} successfully, you are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)