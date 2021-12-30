from todoapp import db
import datetime
# after create a relation with category!
today = datetime.datetime.today()
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String, nullable=False, default='tasks')
    date = db.Column(db.String, default='')
    add_date = db.Column(db.DateTime, default=today, nullable =False)
    start = db.Column(db.DateTime)
    completed = db.Column(db.DateTime)

# category show/hide
# create relation

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(250, nullable=False))
#     show = db.Column(db.Boolean, default=True)
