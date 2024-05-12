from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Project, User

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
@main.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if current_user.role == "Administrator":
        return redirect(url_for('admins.admin_dashboard'))
    
    users = User.query.order_by(User.last_name).all()
    projects = Project.query.order_by(Project.date_created).all()
    
    
    return render_template('dashboard.html', title='Home', users=users, projects=projects)

@main.route('/about', methods=['POST', 'GET'])
@login_required
def about():
    return render_template('about.html', title='Home')