from flask import render_template, url_for, request, redirect, flash
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Project
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        project_title = request.form['title']
        new_project = Project(title=project_title)
        
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'Error adding project'
        
    else:
        projects = Project.query.order_by(Project.date_created).all()
        return render_template('index.html', projects = projects, title='Home')
    
@app.route('/delete/<int:id>')
def delete(id):
    project_to_delete = Project.query.get_or_404(id)
    
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'Error deleting project'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    project = Project.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        project.budget = request.form['budget']
        
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Error updating project"
    else:
        return render_template('update.html', project = project, title='Update')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, department=form.department.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash(f'Email already exists', 'danger')
            return redirect(url_for('register'))

        
        flash(f'Account created for {form.email.data} successfully, you are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login failed, incorrect email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('User logged out, please log in', 'info')
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.department = form.department.data
        current_user.email = form.email.data
        
        try:
            db.session.commit()
            flash(f'Account updated successfully', 'success')
        except:
            flash(f'Error updating account information', 'danger')
            
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.department.data = current_user.department
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)