from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from terminal import get_command

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String, nullable=False, default='Tasks')

# get_categories function checks for all categories from db and returns a list witch contains unique categories


def get_categories():
    # not really efficient way ....
    categories = []
    for category in db.session.query(Tasks).distinct():
        categories.append(category.category)
    unique_dict = set(categories)
    unique_list = list(unique_dict)
    return unique_list


def return_back():
    # return back function redirects to main page or to category page
    # checking if redirected from category menu (main page)
    # if task completed button pressed from category menu return to this category
    if request.args.get('category') is not None:
        return redirect(url_for('show_category', name=request.args.get('category')))
    return redirect(url_for('home_page'))


def is_task_completed(boolean):
    # function takes boolean as argument using in completed and undo section
    # getting task id from id arg
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
    categories = get_categories()
    for category in categories:
        # adding to todo_list dict all tasks related to this category
        todo_list[category] = Tasks.query.filter_by(category=category).all()
    # calling get_categories two times !!! not efficient
    return render_template('index.html', todo_list=todo_list, categories=categories)


@app.route('/completed')
def completed():
    is_task_completed(True)
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


@app.route('/undo')
def undo():
    is_task_completed(False)
    return return_back()


@app.route('/terminal', methods=['POST'])
def terminal():
    users_input = request.form.get('add')
    # check_input can be named as check_for_command
    # it check for a command in the terminal if command exist it will check all possible commands
    # else it will just add to current active category
    check_input = get_command(users_input)
    if len(check_input) > 0:
        # if category word in terminal bar then user created or added to this category something
        if 'Main' in check_input:
            return redirect(url_for('home_page'))

        elif 'Open' in check_input:
            if len(users_input.split()) < 2:
                return redirect(url_for('home_page'))
            cat_name = users_input.split()[1]
            return redirect(url_for('show_category', name=cat_name))

        elif 'Rename' in check_input:
            # rename category_name new_name
            check_input = users_input.split()
            if len(users_input) < 3:
                return redirect(url_for('home_page'))

            category_rename = check_input[1]
            category_new_name = check_input[2]
            print(category_rename)
            print(category_new_name)
            # getting all tasks from db related to old category
            tasks_with_category = Tasks.query.filter_by(category=category_rename).all()
            print(tasks_with_category)
            # assigning an new category name to all task from db
            for task in tasks_with_category:
                task.category = category_new_name
                db.session.commit()
            if request.args.get('category') is not None:
                return redirect(url_for('show_category', name=category_new_name))
            return redirect(url_for('home_page'))

        else:
            # in the future it will be help menu
            return redirect(url_for('home_page'))

    else:
        # checking for category name if category is none it means task will be added to Tasks section
        # Task is default name if task create without category name
        if request.args.get('category') is not None:
            print('adding to')
            print(request.args.get('category'))
            task = Tasks(task=request.form.get('add'), category=request.args.get('category'))
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('show_category', name=request.args.get('category')))

        else:
            # if all others are missed = main page and just add the new task
            task = Tasks(task=request.form.get('add'))
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('home_page'))


@app.route('/category/<name>')
def show_category(name):
    print(name)
    print(name.capitalize())
    current_category_todo = Tasks.query.filter_by(category=name).all()
    print(current_category_todo)
    return render_template('category.html', category_name=name, todo_list=current_category_todo)


if __name__ == '__main__':
    app.run(debug=True)
