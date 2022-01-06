from datetime import datetime, date
from flask import request, render_template, redirect, url_for
from todoapp.models import Tasks
from todoapp.db_actions import DbActions

# class DateOutput:
#     def __init__(self, deadline_date):
#         self.deadline = datetime.strptime(deadline_date, '%Y-%m-%d').date()
#         delta = self.deadline - date.today()
#         self.delta = int(delta.days)    

#     def modify_date(self):

#         if self.delta == 0:
#             return 'Today'
#         elif self.delta == 1:
#             return 'Tomorrow'
#         elif self.delta < 0:
#             return f'{self.deadline} !!!'
#         else:
#             return self.deadline
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


def get_tasks(category):
    if request.args.get('sort') != None:
        sort_value = request.args.get('sort')
        if sort_value == 'deadlines':
            tasks = DbActions.get_category_tasks_deadlines(category.id)
            tasks = tasks.order_by(Tasks.date)
        elif sort_value == 'optional':
            tasks = DbActions.get_category_optional_tasks(category.id)
            tasks = tasks.order_by(Tasks.date)
    else:
        tasks = DbActions.get_all_category_tasks(category)
    
    return tasks


# name!
def return_category_show(name):
    category = DbActions.get_category(name)

    if category is None:
        return redirect(url_for('dashboard.home_page'))

    tasks = get_tasks(category)

    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('category.html', category_name=name, 
        todo_list=tasks, get_deadline= calculate_deadline)


def return_show_deadline(name):

    category = DbActions.get_category(name)

    if category is None:
        return redirect(url_for('dashboard.home_page'))

    tasks = DbActions.get_category_tasks_deadlines(category.id).order_by(Tasks.date)
    unique_dates = tasks.distinct(Tasks.date).group_by(Tasks.date)
    
    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('list.html', category_name=name, 
        todo_list=tasks, get_deadline= date_output, dates = unique_dates)
