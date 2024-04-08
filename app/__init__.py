from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '6180ef2e8b8de6550815398689b9513a16e63f1a8635a6f87a192de2959419f9'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ppms?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

from app import routes