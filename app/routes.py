from flask import render_template, url_for, request, redirect, flash, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm
from app.models import User, Project
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods=['POST', 'GET'])
@app.route('/projects', methods=['POST', 'GET'])
@login_required
def index():
    projects = Project.query.order_by(Project.date_created).filter_by(submitter=current_user)
    return render_template('index.html', projects = projects, title='Home')
    
@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user:
        abort(403)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except:
        flash('Error deleting project', 'success')
    return redirect(url_for('index'))
    
@app.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user:
        abort(403)
    
    return render_template('project.html', title=project.title, project=project)
    
@app.route('/project/<int:project_id>/update', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user:
        abort(403)
    form = ProjectForm()
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.budget = form.budget.data
        project.initial_mode = form.initial_mode.data
        project.date_needed = form.date_needed.data
        project.source = form.source.data
        project.category = form.category.data
        
        try:
            db.session.commit()
            flash('Project updated successfully', 'success')
        except:
            flash('Error updating account information', 'danger')

        return redirect(url_for('project', project_id=project.id))
    
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.budget.data = project.budget
        form.initial_mode.data = project.initial_mode
        form.date_needed.data = project.date_needed
        form.source.data = project.source
        form.category.data = project.category

    return render_template('edit_project.html', title='Update Project', form=form, legend='Update Project')

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
            flash('Email already exists', 'danger')
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
@login_required
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
            flash('Account updated successfully', 'success')
        except:
            flash('Error updating account information', 'danger')
            
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.department.data = current_user.department
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route('/projects/new', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data, description=form.description.data, budget=form.budget.data, initial_mode=form.initial_mode.data, date_needed=form.date_needed.data, source=form.source.data, category=form.category.data, submitter=current_user)
        try:
            db.session.add(project)
            db.session.commit()
        except:
            flash('Error creating project', 'danger')
            return redirect(url_for('create_project'))
        flash('Project created successfully', 'success')
        return redirect(url_for('index'))
    
    form.budget.data = 0.00
    return render_template('edit_project.html', title='New Project' , form=form, legend='New Project')