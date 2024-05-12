from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Project, User
from sqlalchemy import *

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
@main.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if current_user.role == "Administrator":
        return redirect(url_for('admins.admin_dashboard'))
    
    users = User.query.order_by(User.last_name).all()
    
    
    approved_status_query = db.session.query(Project.status,
                      func.count(Project.id).label('projects_count'),
                      func.sum(Project.budget).label('total_budget')
                        ).join(User).group_by(Project.status).filter(Project.user_id==current_user.id).filter(Project.status=="Approved")
    
    pending_status_query = db.session.query(Project.status,
                      func.count(Project.id).label('projects_count'), 
                      func.sum(Project.budget).label('total_budget')
                        ).join(User).group_by(Project.status).filter(Project.user_id==current_user.id).filter(Project.status=="Pending")
    
    rejected_status_query = db.session.query(Project.status,
                      func.count(Project.id).label('projects_count'), 
                      func.sum(Project.budget).label('total_budget')
                        ).join(User).group_by(Project.status).filter(Project.user_id==current_user.id).filter(Project.status=="Rejected")
    
    return render_template('dashboard.html', title='Home', users=users, a_query = approved_status_query, p_query = pending_status_query, r_query = rejected_status_query)

@main.route('/about', methods=['POST', 'GET'])
@login_required
def about():
    return render_template('about.html', title='Home')