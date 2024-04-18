from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Project, User
from app.admin.forms import ProjectStatusUpdateForm

admins = Blueprint('admins', __name__)


@admins.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.role == "Administrator":
        return abort(403)
    
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@admins.route('/admin/projects', methods=['GET', 'POST'])
@login_required
def admin_projects():
    if not current_user.role == "Administrator":
        return abort(403)
    
    projects = Project.query.order_by(Project.date_created).all()
    return render_template('admin/projects_list.html', projects = projects ,title='Submitted Projects')

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