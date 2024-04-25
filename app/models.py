from datetime import datetime
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.DECIMAL(14,2), nullable=False, default=0.00)
    initial_mode = db.Column(db.String(200), nullable=False)
    date_needed = db.Column(db.DateTime, nullable=False)
    source = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), nullable=False, default="Pending")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Project('{self.id}', '{self.title}', '{self.status}')"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False, default="None")
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    role = db.Column(db.String(20), nullable=False, default="Head")
    
    projects = db.relationship('Project', backref='submitter', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
    
