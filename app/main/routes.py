from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app.models import Project

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
@main.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    if current_user.role == "Administrator":
        return redirect(url_for('admins.admin_dashboard'))
    return render_template('dashboard.html', title='Home')

@main.route('/about', methods=['POST', 'GET'])
@login_required
def about():
    return render_template('about.html', title='Home')