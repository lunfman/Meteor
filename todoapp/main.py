import re
from flask import Flask, render_template, request, redirect, url_for
from models import db, Tasks
from terminal import Manager
from datetime import date, datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# init terminal class
terminal_logic = Manager(db)

def return_back():
    """
    return_back function checks if request made from category tab ('/category/name') or from main menu ('/')
    if made from category -> redirect back to this category
    category value located in templates/category.html
    href={{url_for('completed', id=todo.id, category=category_name)}}
    """
    if request.args.get('category') is not None:
        # url_for takes name as an argument because show_category route = /category/<name>
        return redirect(url_for('show_category', name=request.args.get('category')))
    return redirect(url_for('home_page'))


def is_task_completed(boolean):

    # function takes boolean as argument
    # function used in completed and undo section
    
    # getting task id from id arg -> id arg comes from template check 
    # return_back function for more info
    task_id = request.args.get('id')
    
    # looking for the task in db by id
    completed_task = Tasks.query.get(task_id)
    
    # changing tasks completed to true
    completed_task.completed = boolean
    
    # saving
    db.session.commit()


def calculate_deadline(deadline):
    
    '''
    this function calculates how many days left till deadline
    and return a string with delta of days
    if one day left it return word like tomorrow.
    soon will add more words if needed
    '''

    # checking if deadline empty or note
    if deadline == '':
        return '-'
   
    # creating data object from deadline argument to calculate two date objs
    # after createing date objs call method date() because date.today is a date!!!
    deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    delta = deadline - date.today()

    delta = int(delta.days)

    if delta == 1:
        return 'tomorrow'
    elif delta == 0:
        return 'today'
    elif delta < 0:
        return 'Failed'
    else:
        return f'{delta} days'


def date_output(deadline):
    deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    delta = deadline - date.today()

    delta = int(delta.days)

    if delta == 0:
        return 'Today'
    elif delta == 1:
        return 'Tomorrow'
    elif delta < 0:
        return f'{deadline} !!!'
    else:
        return deadline




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
