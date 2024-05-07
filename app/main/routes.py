from flask import render_template, request, Blueprint
from flask_login import login_required
from app.models import Project

main = Blueprint('main', __name__)

@main.route('/user_dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Home')

@main.route('/about', methods=['POST', 'GET'])
@login_required
def about():
    return render_template('about.html', title='Home')