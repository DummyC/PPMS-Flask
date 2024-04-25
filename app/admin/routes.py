from flask import render_template, url_for, flash, redirect, request, abort, send_file, Blueprint
from flask_login import current_user, login_required
from app import db, bcrypt
from app.models import Project, User
from app.admin.forms import ProjectStatusUpdateForm, CreateUserForm, UpdateUserForm
from app.admin.utils import generate_app_xlsx
from io import BytesIO
import os

admins = Blueprint('admins', __name__)

# dashboard routes

@admins.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.role == "Administrator":
        return abort(403)
    
    return render_template('admin/dashboard.html', title='Admin Dashboard')

# project routes

@admins.route('/admin/projects', methods=['GET', 'POST'])
@login_required
def admin_projects():
    if not current_user.role == "Administrator":
        return abort(403)
    
    projects = Project.query.order_by(Project.date_created).all()
    return render_template('admin/projects_list.html', projects = projects ,title='Submitted Projects')

@admins.route('/admin/projects/generate', methods=['GET', 'POST'])
@login_required
def admin_generate_app():
    if not current_user.role == "Administrator":
        return abort(403)
    
    if os.path.exists("tmp/APP.xlsx"):
        os.remove("tmp/APP.xlsx")
    
    projects = Project.query.order_by(Project.category).filter_by(status="Approved")
    generate_app_xlsx(projects)
    
    with open("tmp/APP.xlsx", "rb") as file:
        read = file.read()
        buffer = BytesIO()
        buffer.write(read)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="APP.xlsx")

@admins.route('/admin/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def admin_project(project_id):
    if not current_user.role == "Administrator":
        return abort(403)
    
    project = Project.query.get_or_404(project_id)
    form = ProjectStatusUpdateForm()
    if form.validate_on_submit():
        project.status = form.status.data
        
        try:
            db.session.commit()
            flash('Project updated successfully', 'success')
        except:
            flash('Error updating account information', 'danger')
        
        return redirect(url_for('admins.admin_project', project_id=project_id))

    elif request.method == 'GET':
        form.status.data = project.status     
        
    return render_template('admin/project.html', title=project.title, form=form, project=project)

@admins.route('/admin/project/<int:project_id>/delete', methods=['POST'])
@login_required
def admin_delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if not current_user.role == "Administrator":
        return abort(403)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except:
        flash('Error deleting project', 'success')
    return redirect(url_for('admins.admin_projects'))

# user management routes

@admins.route('/admin/users', methods=['POST', 'GET'])
@login_required
def users_list():
    users = User.query.order_by(User.last_name).all()
    if not current_user.role == "Administrator":
        return abort(403)
    
    return render_template('admin/users_list.html', title='Users', users = users)

@admins.route('/admin/users/create', methods=['POST', 'GET'])
@login_required
def create_user():
    if not current_user.role == "Administrator":
        return abort(403)
    
    form = CreateUserForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, department=form.department.data, email=form.email.data, password=hashed_password, role=form.role.data)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('Email already exists', 'danger')
            return redirect(url_for('users.register'))

        
        flash(f'Account created for {form.email.data} successfully', 'success')
        return redirect(url_for('admins.users_list'))
    
    return render_template('admin/create_user.html', title='Create User', form=form)

@admins.route('/admin/user/<int:user_id>/update', methods=['POST', 'GET'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.role == "Administrator":
        return abort(403)
    
    form = UpdateUserForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.department = form.department.data
        user.email = form.email.data
        user.role = form.role.data
        
        try:
            db.session.commit()
            flash('User updated successfully', 'success')
        except:
            flash('Error updating account information', 'danger')
            
        return redirect(url_for('admins.users_list'))
    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.department.data = user.department
        form.email.data = user.email
        form.role.data = user.role
        
    return render_template('admin/update_user.html', title='Update User', form=form, user=user)

@admins.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.role == "Administrator":
        return abort(403)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
    except:
        flash('Error deleting user', 'danger')
    return redirect(url_for('admins.users_list'))

