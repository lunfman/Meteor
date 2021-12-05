from flask import request, redirect, url_for
from .date_manage import manageDeadlines
from .models import db, Tasks

class Terminal:


    # how it is going to work? Users type something in the terminal. Flask receive message and send it 
    # to Terminal class
    # 1) Get commands from the input to validate what user want to do
    # 2) After do what user wants
    # 3) Return whatever needed 


    def __init__(self):
        # commands which using our app for interacting with the system/app
        # strict names
        self.commands = ['Open', 'Rename', 'Main', 'Create', 'Add', 'By', 'In']
        # date_validator uses manageDeadlines class form date_manage this module not reusable
        # made for this app
        self.date_validator = manageDeadlines()
        # input is going to store users input  do we need it???
        self.input = ''
        # cur_commands is going to store recent commands from using the class
        self.cur_commands = []


    def get_command(self, search):
        # cleaning cur_commands array before checking
        # because this list should contain only latest commands
        self.cur_commands = []
        # takes one argument -> string -> users input in terminal
        # get command function looking for commands in the users input and creates a list of commands
        # why? split to separate values of the input and find commands
        for command in search.split():
            if command in self.commands:
                # appending commands to cur_commands
                self.cur_commands.append(command)
        return self


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

def add_deadline(users_input):
    return date_validator.check_date(users_input)


def show_current():
    pass

def add_many():
    pass

# by_next = add_deadline('By next month')
# by_num = add_deadline('By 12')
# by_month = add_deadline('By february')
# by_month_dat = add_deadline('By 3 March')
# print(by_next)
# print(by_num)
# print(by_month)
# print(by_month_dat)