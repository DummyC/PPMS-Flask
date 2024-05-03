import os

class Config:
    
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/ppms?charset=utf8mb4'
    # use sqlite for development 
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_SERVER_EMAIL')
    MAIL_PASSWORD = os.environ.get('MAIL_SERVER_PASSWORD')