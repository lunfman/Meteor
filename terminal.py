from flask import request, redirect, url_for

# now list is useless but soon when i decide to add more complex logic it will be handy
commands = ['Open', 'Rename', 'Main']


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
