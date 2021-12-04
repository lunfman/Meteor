from flask_sqlalchemy import SQLAlchemy

# after create a relation with category!
db = SQLAlchemy()

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String, nullable=False, default='Tasks')
    date = db.Column(db.String, default='')
