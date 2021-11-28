# search = '<test open_cat> flat'
# search = 'Open Hes'
from flask import Flask, render_template, request, redirect, url_for
# get command function looking for commands in the users input and return list of commands
# now list is useless but soon when i decide to add more complex logic it will be handy

commands = ['Open', 'Rename', 'Main']


def get_command(search):
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
    # rename category_name new_name -> Rename old_name new_name
    check_input = users_input.split()
    if len(users_input.split()) == 3:
        category_rename = check_input[1]
        category_new_name = check_input[2]
        # getting all tasks from db related to old category
        tasks_with_category = tasks.query.filter_by(category=category_rename).all()
        # assigning an new category name to all task from db
        for task in tasks_with_category:
            task.category = category_new_name
            db.session.commit()
        if request.args.get('category') is not None:
            return redirect(url_for('show_category', name=category_new_name))
        return redirect(url_for('home_page'))
    return redirect(url_for('home_page'))
