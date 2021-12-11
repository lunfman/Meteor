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

@app.route('/')
def home_page():

    # categories names
    categories = (Tasks.query.distinct(Tasks.category).group_by(Tasks.category))
    # categories data -> key category:name and after {} -> {cat_name:{cat_data:}}
    cat_data = {}
   
    for category in categories:
        # new_dict for storeing extracted data
        new_dict = {}
        by_today =  Tasks.query.filter(Tasks.category == category.category, Tasks.date == date.today()).count()
        #print(f'By today {by_today}')
        # dates for tomorrow
        new_dict['today'] = by_today
        by_tomorrow = Tasks.query.filter(Tasks.category == category.category, Tasks.date == date.today() + timedelta(days=1)).count()
        #print(f'By tomorrow {by_tomorrow}')
         # tasks in category
        new_dict['tomorrow'] = by_tomorrow
        # total tasks
        tasks_number = Tasks.query.filter(Tasks.category == category.category).count()
        #print(f'Number of tasks {tasks_number}')
        new_dict['tasks'] = tasks_number
        # completed tasks in category
        tasks_comp_number = Tasks.query.filter(Tasks.category == category.category, Tasks.completed == True).count()
        #print(f'Number of completed tasks {tasks_comp_number}')
        new_dict['completed'] = tasks_comp_number
        # expired tasks
        expired =  Tasks.query.filter(Tasks.category == category.category, Tasks.date != '' ,Tasks.date < date.today()).count()
        #print(f'expired : {expired}')
        new_dict['expired'] = expired
        # not completed and without deadlines
        no_deadlines = Tasks.query.filter(Tasks.category == category.category, Tasks.date == '', Tasks.completed == False).count()
        #print(f'Tasks without deadline and not completed: {no_deadlines}')
        new_dict['ordinary'] = no_deadlines
        # saveing extracted data to cat_data with category name as key
        cat_data[category.category] = new_dict
    #print(cat_data)
    return render_template('index.html', categories=categories, data=cat_data)


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
        parameter = request.args.get('sort')
        if parameter == 'deadlines':
            current_category_todo = (Tasks.query.filter(Tasks.category == name, Tasks.date != '')
                .order_by(Tasks.date))
        elif parameter == 'optional':
            current_category_todo = (Tasks.query.filter(Tasks.category == name, Tasks.date == '')
                .order_by(Tasks.date))   
    else:
        current_category_todo = (Tasks.query.filter(Tasks.category == name))
    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('category.html', category_name=name, 
        todo_list=current_category_todo, get_deadline= calculate_deadline)


@app.route('/category/<name>/list')
def show_deadlines(name):
    # looking for tasks in this category and makeing sure it has date
    current_category_todo = (Tasks.query.filter(Tasks.category == name, Tasks.date != '')
    .order_by(Tasks.date))
    # unique_dates = db.session.query(Tasks).distinct(Tasks.category).group_by(Tasks.category)
    # getting unique dates for this cat from db
    un_dates = current_category_todo.distinct(Tasks.date).group_by(Tasks.date)
    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('list.html', category_name=name, 
        todo_list=current_category_todo, get_deadline= date_output, dates = un_dates)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
