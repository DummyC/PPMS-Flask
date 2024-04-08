from flask import render_template, url_for, request, redirect, flash
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Project

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data} successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.email.data == 'example@example.com' and form.password.data == 'password'):
            flash('Login success', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed, incorrect email or password', 'danger')
    return render_template('login.html', title='Login', form=form)
