from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Decimal(14,2))
    initial_mode = db.Column(db.String(200))
    status = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Project %r>' % self.id
    
    
    


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        project_title = request.form['title']
        new_project = Projects(title=project_title)
        
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error adding project'
        
    else:
        projects = Projects.query.order_by(Projects.date_created).all()
        return render_template('index.html', projects = projects)
    
@app.route('/delete/<int:id>')
def delete(id):
    project_to_delete = Projects.query.get_or_404(id)
    
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting project'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    project = Projects.query.get_or_404(id)
    
    if request.method == 'POST':
        project.title = request.form['title']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error updating project"
    else:
        return render_template('update.html', project = project)

if __name__ == "__main__":
    # with app.app_context:
    #     db.create_all()
    app.run(debug=True) 