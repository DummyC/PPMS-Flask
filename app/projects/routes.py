from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db
from app.models import Project
from app.projects.forms import ProjectForm

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=['POST', 'GET'])
@login_required
def projects_list():
    projects = Project.query.order_by(Project.date_created).filter_by(submitter=current_user)
    return render_template('projects_list.html', projects = projects, title='Projects')
    
    
@projects.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user:
        abort(403)
    
    return render_template('project.html', title=project.title, project=project)
    
@projects.route('/projects/new', methods=['GET', 'POST'])
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
            return redirect(url_for('projects.create_project'))
        flash('Project created successfully', 'success')
        return redirect(url_for('projects.projects_list'))
    
    form.budget.data = 0.00
    return render_template('edit_project.html', title='New Project' , form=form, legend='New Project')

@projects.route('/project/<int:project_id>/update', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user or project.status == "Approved":
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

        return redirect(url_for('projects.project', project_id=project.id))
    
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.budget.data = project.budget
        form.initial_mode.data = project.initial_mode
        form.date_needed.data = project.date_needed
        form.source.data = project.source
        form.category.data = project.category

    return render_template('edit_project.html', title='Update Project', form=form, legend='Update Project')

@projects.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.submitter != current_user or project.status == "Approved":
        abort(403)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except:
        flash('Error deleting project', 'danger')
    return redirect(url_for('projects.projects_list'))