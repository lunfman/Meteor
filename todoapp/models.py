from enum import unique
from todoapp import db
import datetime

today = datetime.datetime.today()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    categories = db.relationship('Category', backref='project', lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), unique=True)
    show = db.Column(db.Boolean, default=True)
    tasks = db.relationship('Tasks', backref='category', lazy=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.String, default='')
    add_date = db.Column(db.DateTime, default=today, nullable =False)
    start_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))