from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from terminal import create_category_add_many, get_command, open_command, rename_command

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String, nullable=False, default='Tasks')


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
    # getting task id from id arg -> id arg comes from template check return_back function for more info
    task_id = request.args.get('id')
    # looking for the task in db by id
    completed_task = Tasks.query.get(task_id)
    # changing tasks completed to true
    completed_task.completed = boolean
    # saving
    db.session.commit()


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
    # get_command functions ->  return list of commands if found or empty list
    check_input = get_command(users_input)
    # if get_command returned empty list -> user added task
    if len(check_input) > 0:
        # Looking for the command
        if 'Main' in check_input:
            return redirect(url_for('home_page'))

        elif 'Open' in check_input:
            return open_command(users_input)

        elif 'Rename' in check_input:
            return rename_command(users_input, db, Tasks)
        
        elif 'Create' and 'Add' in check_input:
            return create_category_add_many(users_input, db, Tasks)

    else:
        # else -> user did not typed any command
        # checking for category name if category is none it means task will be added to Tasks section
        # Task is default name if task create without category name
        if request.args.get('category') is not None:
            print('adding to')
            print(request.args.get('category'))
            # Creating a new Task with category name
            task = Tasks(task=request.form.get('add'), category=request.args.get('category'))
            # adding new Task to db
            db.session.add(task)
            # save
            db.session.commit()
            # redirecting back to the category from which request came
            return redirect(url_for('show_category', name=request.args.get('category')))

        else:
            # save task to Tasks category -> Default
            task = Tasks(task=request.form.get('add'))
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('home_page'))


@app.route('/category/<name>')
def show_category(name):
    # looking for tasks in this category
    current_category_todo = Tasks.query.filter_by(category=name).all()
    # return page with category name and tasks
    return render_template('category.html', category_name=name, todo_list=current_category_todo)


if __name__ == '__main__':
    app.run(debug=True)
