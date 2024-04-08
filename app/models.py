from datetime import datetime
from app import db

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
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    projects = db.relationship('Project', backref='submitter', lazy=True)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"
