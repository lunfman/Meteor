try:
    from .date_manage import manageDeadlines
    from .models import Tasks
except:
    from date_manage import manageDeadlines
    from models import Tasks

from flask import redirect, url_for, request
from werkzeug.wrappers import response

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

class Terminal:
    
    '''
    Terminal class allows to get users command from the input
    by using validate_input method
    '''

    # How it is going to work? 
    # Users type something in the terminal.
    # Flask receive message and send it to Terminal class for validation
    # When validation complete terminal class return value or values
    # If data was in the wrong format return None
    # Else return data


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

        # self.input -> = search -> store current search value
        # get command is the first running method in validation
        # thats why self.input = search
        self.input = search
        
        # why? split to separate values of the input and find commands
        for command in search.split():
            if command in self.commands:
                # adding commands to cur_commands
                self.cur_commands.append(command)
        return self


    def open_command(self):   
        # Open -> cat => strict category
        
        # category [0]-> because command_extractor return a list
        category = self.command_extractor('Open')[0]
        
        # return category as a string
        return category


    def rename_command(self):

        # -> Rename old category To new category
        # rename has two commands Rename and To

        # command_extractor return -> ['old cat', 'new_cat']
        return  self.command_extractor('Rename', 'To')

            # redirects
            # check return_back() in main.py for more info
        #     if request.args.get('category') is not None:
        #         return redirect(url_for('show_category', name=category_new_name))
        #     return redirect(url_for('home_page'))
        # return redirect(url_for('home_page'))


    def create_category_add_many(self):

        # Create 'Category Name' Add 'Task1', 'Task2', ETC
        # method return an list with category name and a list of tasks
        # command_extractor return -> [category name, to dos]

        return self.command_extractor('Create', 'Add') 
    

    def add_deadline(self):
        # add deadline method returns all tasks and date
        
        # extracting tasks from the input
        # index 0 in this scenario everythin before By
        tasks = self.input.split('By')[0]
        
        # creating a tasks list from tasks
        tasks_list = [task.strip() for task in tasks.split(',')]
        return [tasks_list, self.date_validator.check_date(self.input)]
   
    def command_extractor(self, *args):

        # this method extract commands from self.input by providing commands
        # which should be removed
        # if input has complex values like add task1 ,task2, task1 task2
        # it will return them as a list
        # otherwise return extracted value

        # example: Create category name Add task1, task2, task3
        # output: ['category name', ['task1', 'task2', 'task3']]

        # example : Open category name
        # output: ['category name']

        # extracted is going to store extracted values
        extracted = []
        
        # clean_input used for manipulating the string cause string immutable
        # and we do not want to manipulate self.input directly !!!!
        clean_input = self.input
        
        #running for loop in args and replace arg value in the string
        for arg in args:
            # also validating data here
            # if arg not in clean_input return None

            # replace arg with !C! to escape problems with users input in the future
            clean_input = clean_input.replace(arg, '!C!')
        # creating clean list by split method    
        clean_list = clean_input.strip().split('!C!')
        # creating an extracted list
        for value in clean_list:
            # if value not equal to empty continue or (empty with spaces this came fro unittesting)
            if value != '' and value != ' ':
                # if value do not have ',' seperator just add value to the list
                if ',' not in value:
                    extracted.append(value.strip())
                else:
                    # if has seperator create a list of values and add to the list
                    # also strip values to get rid of bad spaces
                    values_list = [value.strip() for value in value.split(',')]
                    extracted.append(values_list)
       
        # return extracted list
        return extracted


    def validate_input(self, input):
        # validate_input method validates input from the app

        # getting all commands from input
        self.get_command(input)

        # making a list from input value via split method
        input_list = self.input.split()

        # Validating data
        # Command like Open, Rename, Create, Main always has to be first!
        if self.cur_commands == ['Open'] and input_list[0] == 'Open':
            return self.open_command()
        elif self.cur_commands == ['Rename', 'To'] and input_list[0] == 'Rename':
            return self.rename_command()
        elif self.cur_commands == ['Create', 'Add'] and input_list[0] == 'Create':
            # if the length oft create_category and many less than 2 -> wrong format
            if len(self.create_category_add_many()) < 2:
                return None
            return self.create_category_add_many()
        elif self.cur_commands == ['By']:
            return self.add_deadline()
        elif self.cur_commands == ['Main']:
            # if Main was used
            return True

        elif len(self.cur_commands) == 0:
            # if command not found user created a task!
            # and validator return input back
            return input

        else:
            return None
    
    
    def show_current():
        pass


    def add_many():
        pass


class terminalLogic():
    '''
    Terminal logic class manages processes after user input was validated 
    It uses almost the same validation as Terminal.validate_input()
    Decided to do it here to avoid bad structure

    Init has one argument -> db -> db from main.py where to store data
    Tasks comes from module.py
    '''
    def __init__(self, db):
        self.terminal = Terminal()
        self.db = db


    def open_command_logic(self, response):
        # method for open command
        return redirect(url_for('show_category', name = response))


    def main_command_logic(self):
        # Main command -> back home
        return redirect(url_for('home_page'))


    def rename_command_logic(self, old_category, new_category):
        
        # looking for tasks with this category
        tasks_with_category = Tasks.query.filter_by(category=old_category).all()
        
        # if tasks_with_category = [] redirect to main page
        if len(tasks_with_category) == 0:
            # redirects
            return return_back()

        # changing category name to new one for all tasks related to old category
        for task in tasks_with_category:
            task.category = new_category
            self.db.session.commit()    
        return return_back()     


    def create_add_many_logic(self, category, tasks):
       # running a loop for every task in tasks and adding new task to db.seession after loop ends
        # save session and redirect to created category
        
        for task in tasks:
            # category = category from func arg
            new_task = Tasks(task=task, category = category)
            self.db.session.add(new_task)
        self.db.session.commit()

        return redirect(url_for('show_category', name=category))

    def exe_command(self, input):
        # this method executes commands
        
        # validating users input by using validate_input method of terminal class 
        # validate can return value / values or none       
        self.response = self.terminal.validate_input(input)
        
        # if respose not none continue
        if self.response:
            print('Checking input')
            # if after validation cur_commands = Open -> Open command used
            # Use Open logic and return
            if self.terminal.cur_commands == ['Open']:
                return self.open_command_logic(self.response)
            # if Main left in cur_commands Main used! use main command logic    
            elif self.terminal.cur_commands == ['Main']:
                print('main')
                return self.main_command_logic()
            elif self.terminal.cur_commands == ['Rename', 'To']:
                print('rename section')
                old_category_name = self.response[0]
                new_category_name = self.response[1]
                return self.rename_command_logic(old_category_name, new_category_name)
            elif self.terminal.cur_commands == ['Create', 'Add']:
                category = self.response[0]
                tasks = self.response[1]
                return self.create_add_many_logic(category, tasks)

            else:
                # else -> user did not typed any command
                # checking for category name if category is none it means task will be added to Tasks section
                # Task is default name if task create without category name
                if request.args.get('category') is not None:
                    print('add cat')
                    # Creating a new Task with category name
                    task = Tasks(task=request.form.get('add'), category=request.args.get('category'))
                    # adding new Task to db
                    self.db.session.add(task)
                    # save
                    self.db.session.commit()
                    # redirecting back to the category from which request came
                    return redirect(url_for('show_category', name=request.args.get('category')))

                else:
                # save task to Tasks category -> Default
                    print('else section')
                    task = Tasks(task=self.response)
                    self.db.session.add(task)
                    self.db.session.commit()
                    return self.main_command_logic()
        else:
            return redirect(url_for('home_page'))
