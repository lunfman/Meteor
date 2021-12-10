from os import name
from types import new_class
from terminalobj import Terminal, Command
from flask import redirect, url_for, request
from models import Tasks
from date_manage import manageDeadlines
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

class Manager:
    def __init__(self, db):
        self.open_command = Command('Open', self.open_command_logic)
        self.main_command = Command('Main', self.main_command_logic)
        self.rename_command = Command(name='Rename', 
            function=self.rename_command_logic, separator='To')
        self.create_command = Command(name='Create',
            function=self.create_command_logic, order=True)
        self.add_command = Command(name='Add',
            function=self.add_command_logic, order=True, separator= ',')
        self.by_command = Command(name='By', order=True, function=self.by_command_logic)
        self.show_command = Command('Show', self.show_command_logic)
            
        self.commands = [self.open_command, self.main_command, self.rename_command,
         self.create_command, self.add_command, self.by_command, self.show_command]
        self.terminal = Terminal(commands=self.commands)
        self.db = db
        self.date_validator = manageDeadlines()
        self.category_name = 'Tasks'
    
    def check_input(self, input):
        # if command found extract command else task was added
        #print(self.terminal.get_command(input).check_for_commands())
        self.category_name=request.args.get('category')
        if self.terminal.get_command(input).check_for_commands():
            return self.terminal.command_extractor()
        else:
            return self.add_task()


    def open_command_logic(self, response):
        if len(response) < 1:
            return redirect(url_for('home_page'))
        return redirect(url_for('show_category', name = ' '.join(response)))

    def main_command_logic(self, response):
        return redirect(url_for('home_page'))

    def add_task(self):
        # checking for category name if category is none it means task will be added to Tasks section
        # Task is default name if task create without category name
        if self.category_name is not None:
            print('add cat')
            # Creating a new Task with category name
            task = Tasks(task=request.form.get('add'), category=request.args.get('category'))
            # adding new Task to db
            self.db.session.add(task)
            # save
            self.db.session.commit()
            # redirecting back to the category from which request came
            return redirect(url_for('show_category', name=self.category_name))

        else:
        # save task to Tasks category -> Default
            print('else section')
            task = Tasks(task=self.terminal._input)
            self.db.session.add(task)
            self.db.session.commit()
            return self.main_command_logic('')    


    def create_command_logic(self, response):
        # create category name
        print('category saved')
        self.category_name = ' '.join(response)
        return redirect(url_for('home_page'))


    def add_command_logic(self, response):
        for task in response:
            print(task, self.category_name)
            new_task = Tasks(task=task, category=self.category_name)
            self.db.session.add(new_task)
        self.db.session.commit()
        print('tasks saved')
        return redirect(url_for('show_category', name=self.category_name))

    def rename_command_logic(self, response):
        old_name = response[0]
        new_name = response[1]
        tasks_with_category = Tasks.query.filter_by(category=old_name).all()
        
        # if tasks_with_category = [] redirect to main page
        if len(tasks_with_category) == 0:
            # redirects
            return return_back()

        # changing category name to new one for all tasks related to old category
        for task in tasks_with_category:
            task.category = new_name
            self.db.session.commit()    
        return return_back()          

    def by_command_logic(self, response):
        task = self.terminal.before_command_string()
        date_string = ' '.join(response)
        deadline = self.date_validator.check_date(date_string)
        new_task = Tasks(task=task, date=deadline, category = self.category_name)
        self.db.session.add(new_task)
        self.db.session.commit()
        return return_back()

    def show_command_logic(self,response):
        print(response)
        if self.category_name is None:
            return redirect(url_for('home_page'))
        elif response[0] == 'deadlines':
            return redirect(url_for('show_deadlines', name=self.category_name, order='test'))
        else:
            return redirect(url_for('home_page'))
        