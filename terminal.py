from os import name
from flask import request, redirect, url_for


# now list is useless but soon when i decide to add more complex logic it will be handy
commands = ['Open', 'Rename', 'Main', 'Create', 'Add']


def get_command(search):
    # get command function looking for commands in the users input and return list of commands
    found_commands = []
    for command in search.split():
        if command in commands:
            found_commands.append(command)
    return found_commands


def open_command(users_input):
    # open -> cat => should be equal to 2 this command can not be combined with others
    if len(users_input.split()) == 2:
        cat_name = users_input.split()[1]
        return redirect(url_for('show_category', name=cat_name))
    return redirect(url_for('home_page'))


def rename_command(users_input, db, tasks):
    # rename needs three arguments users_input , db and Task Model
    # Example: Rename category_name new_name or Rename old_name new_name
    check_input = users_input.split()
    if len(users_input.split()) == 3:
        # if user typed everything right
        # category to rename has index 1
        category_rename = check_input[1]
        # new name of the category has index 2
        category_new_name = check_input[2]
        # getting all tasks from db related to old category
        # if user type category which do not exists query returns empty array
        tasks_with_category = tasks.query.filter_by(category=category_rename).all()

        # if tasks_with_category = [] redirect to main page
        if len(tasks_with_category) == 0:
            # redirects
            if request.args.get('category') is not None:
                return redirect(url_for('show_category', name=category_new_name))
            return redirect(url_for('home_page'))

        # changing category name to new one for all tasks related to old category
        for task in tasks_with_category:
            task.category = category_new_name
            db.session.commit()
        # redirects
        # check return_back() in main.py for more info
        if request.args.get('category') is not None:
            return redirect(url_for('show_category', name=category_new_name))
        return redirect(url_for('home_page'))
    return redirect(url_for('home_page'))

def create_category_add_many(users_input, db, Tasks):
    
    # create_category_add_many takes 3 arguments: 
    #   user_input - > input from terminal
    #   db -> working db
    #   Tasks -> Module for createing tasks

    # Create 'Category Name' Add 'Task1', 'Task2', ETC
    # Extracting category_name from users input -> Split to separate all elements
    # after this method category has index of 1 -> choose this element -> category extracted
    category_name = users_input.split()[1]
    # Why changeing Add to ','? Allows to simplify work  after split method 
    # and not working with nested lists
    # After doing a split to separate parts of the string and start list from index 1
    # in this case Create Name has index 0
    tasks = users_input.replace('Add', ',').split(',')[1:]
    # running a loop for every task in tasks and adding new task to db.seession after loop ends
    # save session and redirect to created category
    for task in tasks:
        new_task = Tasks(task=task, category =category_name)
        db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('show_category', name=category_name))