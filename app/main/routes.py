from flask import render_template, request, Blueprint
from app.models import Project

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html', title='Home')

@main.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html', title='Home')