from flask import render_template, request, Blueprint
from app.models import Project

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
def home():
    return render_template('base.html', title='Home')

@main.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('base.html', title='Home')