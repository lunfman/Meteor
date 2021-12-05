from flask import request, redirect, url_for
from .date_manage import manageDeadlines
from .models import db, Tasks

class Terminal:
    
    '''
    Terminal class allows to manage users inputs from the app
    '''

    # how it is going to work? Users type something in the terminal.
    #  Flask receive message and send it to Terminal class
    # 1) Get commands from the input to validate what user want to do
    # 2) After do what user wants
    # 3) Return whatever needed 


    def __init__(self):
        
        # commands which using our app for interacting with the system/app
        # strict names
        self.commands = ['Open', 'Rename', 'Main', 'Create', 'Add', 'By', 'In', 'To']
        
        # date_validator uses manageDeadlines class form date_manage this module not reusable
        # made for this app
        self.date_validator = manageDeadlines()
        
        # input is going to store users input
        self.input = ''
        
        # cur_commands is going to store recent commands from using the class
        self.cur_commands = []


    def get_command(self, search):
        
        # takes one argument -> string -> users input in terminal
        # get command function looking for commands 
        # in the users input and creates a list of commands
        
        # cleaning cur_commands array before checking
        # because this list should contain only latest commands
        self.cur_commands = []
        
        # why? split to separate values of the input and find commands
        for command in search.split():
            if command in self.commands:
                # adding commands to cur_commands
                self.cur_commands.append(command)
        return self


    def open_command(self):

        # Open -> cat => strict category
        # if after split method list not greater than 1 it means only Open command
        # was provided in input filed
        # if greater using slice method to get category
        
        # using split
        clean_input = self.input.split()

        # if statement also validates if input > 1 and command in commands
        # because Open can be written in lowercase
        if len(clean_input) > 1 and clean_input[0] in self.commands :
            
            # using join with space as seperator to get string 
            # from the sliced list because method has to return string
            cat_name = ' '.join(clean_input[1:])
            
            return cat_name
        return None


    def rename_command(self):

        # -> Rename old category To new category
        # rename has two commands Rename and To

        # Rename task1 To task2 -> now we need to get rid of Rename and To
        # going to use replace method to replace commands 
        # Rename replace with 'C' -> C for command
        # Maybe a better option exists for this operation??!!
        check_input = self.input.replace('To', 'C').replace('Rename', 'C')
        
        # and now split by ',' to get two category names
        # after this split check_input list should have 3 elements -> '', task1, task2
        check_input = check_input.split('C')
       
        # if checking input equal to 3 -> user provided legit data
        # Less means bad request and return None
        if len(check_input) == 3:
            
            # if user typed everything right
            # category to rename has index 1
            # and also need to do strip to get rid of bad spaces
            category_rename = check_input[1].strip()
            
            # new name of the category has index 2
            category_new_name = check_input[2].strip()

            # return a list of values for renaming
            return [category_rename, category_new_name]  
        return None  

            # redirects
            # check return_back() in main.py for more info
        #     if request.args.get('category') is not None:
        #         return redirect(url_for('show_category', name=category_new_name))
        #     return redirect(url_for('home_page'))
        # return redirect(url_for('home_page'))

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


# db logic from rename method
            # tasks_with_category = tasks.query.filter_by(category=category_rename).all()

            # # if tasks_with_category = [] redirect to main page
            # if len(tasks_with_category) == 0:
            #     # redirects
            #     if request.args.get('category') is not None:
            #         return redirect(url_for('show_category', name=category_new_name))
            #     return redirect(url_for('home_page'))

            # # changing category name to new one for all tasks related to old category
            # for task in tasks_with_category:
            #     task.category = category_new_name
            #     db.session.commit()