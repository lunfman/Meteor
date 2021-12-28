from . import category
from flask import request, render_template
from todoapp.models import Tasks
from .logic import calculate_deadline, date_output

@category.route('/category/<name>')
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

@category.route('/category/<name>/list')
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