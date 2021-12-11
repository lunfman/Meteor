from flask import Flask, render_template, request, redirect, url_for
from models import db, Tasks
from terminal_test import Manager
from datetime import date, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# init terminal class
terminal_logic = Manager(db)

def get_categories():
    # get_categories function checks for all categories from db
    # returns a list witch contains unique categories
    categories = []
    try:
        for category in db.session.query(Tasks).distinct():
            categories.append(category.category)    
        unique_dict = set(categories)
        unique_list = list(unique_dict)
        return unique_list
    # except if db do not exists -> first run or deleted
    except:
        db.create_all()
        return []


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
    elif delta < 0:
        return 'Failed'
    else:
        return f'{delta} days'


@app.route('/')
def home_page():
    todo_list = {}
    # Getting categories names
    categories = get_categories()
    for category in categories:
        # adding to todo_list dict all tasks related to this category
        # result -> Task : ['Task1', 'Task2']
        todo_list[category] = Tasks.query.filter_by(category=category).all()
    return render_template('index.html', todo_list=todo_list, categories=categories)


@app.route('/completed')
def completed():
    is_task_completed(True)
    return return_back()


@app.route('/undo')
def undo():
    is_task_completed(False)
    return return_back()


@app.route('/delete')
def delete():

    # getting id from jinja template
    task_id = request.args.get('id')
    
    # looking for the task by id
    task_to_delete = Tasks.query.get(task_id)
    
    # deleting task from db
    db.session.delete(task_to_delete)
    
    # saving
    db.session.commit()
    return return_back()


@app.route('/terminal', methods=['POST'])
def terminal():
    # move this logic to terminal.py when completed
    users_input = request.form.get('add')
    return terminal_logic.check_input(users_input)


@app.route('/category/<name>')
def show_category(name):
    # looking for tasks in this category
    print(request.args.get('sort'))
    if request.args.get('sort') != None:
        if request.args.get('sort') == 'deadlines':
            current_category_todo = (Tasks.query.filter(Tasks.category == name, Tasks.date != '')
                .order_by(Tasks.date))
    else:
        current_category_todo = (Tasks.query.filter(Tasks.category == name))
    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('category.html', category_name=name, 
        todo_list=current_category_todo, get_deadline= calculate_deadline)


# @app.route('/category/<name>/deadlines')
# def show_deadlines(name):
#     # looking for tasks in this category
#     current_category_todo = (Tasks.query.filter(Tasks.category == name, Tasks.date != '')
#     .order_by(Tasks.date))
#     print(request.args)
#     # return page with category name and tasks
#     # passing calculate_deadline function to get_deadline which will be used
#     # inside of category.html template for fetching deadlines
#     return render_template('category.html', category_name=name, 
#         todo_list=current_category_todo, get_deadline= calculate_deadline)



if __name__ == '__main__':
    app.run(debug=True)
