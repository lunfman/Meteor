from todoapp.utilities import DateOutput
from flask import request, render_template, redirect, url_for
from todoapp.models import Tasks
from todoapp.db_actions import DbActions
    

def get_deadline_date(deadline):
    date_name = DateOutput(deadline)
    return date_name.modify_deadline_date()


def get_category_date(deadline):
    if deadline == '':
        return '-'
    date_name = DateOutput(deadline)
    return date_name.modify_category_date()


def get_tasks(category):
    print(request.args.get('sort'))
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


def make_category_show(name):
    category = DbActions.get_category(name)

    if category is None:
        return redirect(url_for('dashboard.home_page'))

    tasks = get_tasks(category)

    # return page with category name and tasks
    # passing calculate_deadline function to get_deadline which will be used
    # inside of category.html template for fetching deadlines
    return render_template('category.html', category_name=name, 
        todo_list=tasks, get_deadline= get_category_date)


def make_show_deadline(name):

    category = DbActions.get_category(name)

    if category is None:
        return redirect(url_for('dashboard.home_page'))
    # move to Dbactions?
    tasks = DbActions.get_category_tasks_deadlines(category.id).order_by(Tasks.date)
    unique_dates = tasks.distinct(Tasks.date).group_by(Tasks.date)

    return render_template('list.html', category_name=name, 
        todo_list=tasks, get_deadline= get_deadline_date, dates = unique_dates)
