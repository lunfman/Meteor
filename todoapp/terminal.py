from os import name
from flask import redirect, url_for, request
from .models import Tasks
from .date_manage import ManageDeadlines
from .some_func import return_back
from . import db


class Terminal:
    def __init__(self, input):

        self.commands = {
            'Open': self.execute_open_function,
            'Rename': self.execute_rename_function,
            'Create': self.create_function,
            'By': self.do_by_function,
            'Main': self.execute_main_function,
            'Show': self.execute_show_function,
            'Add': self.execute_add_function}

        self.input = input
        self.input_split = self.input.split()

        self.category_name = request.args.get('category')
    
    def check_input(self):
        for key in self.commands.keys():
            if key in self.input:
                return self.commands.get(key)()
        
        return self.add_task()
        
        
    def execute_main_function(self):
        return redirect(url_for('dashboard.home_page'))


    def execute_open_function(self):
        category_name = self.input_split[1:]
        return redirect(url_for('category.show_category', name = ' '.join(category_name).lower()))


    def execute_rename_function(self):
        if 'To' in self.input_split:
            index_of_to = self.input_split.index('To')
            old_category = self.input_split[1:index_of_to]
            old_category = ' '.join(old_category)
            new_category = self.input_split[index_of_to+1:]
            new_category = ' '.join(new_category)

            tasks_with_category = Tasks.query.filter_by(category=old_category).all()
        
            # if tasks_with_category = [] redirect to main page
            if len(tasks_with_category) == 0:
                # redirects
                return return_back()

            # changing category name to new one for all tasks related to old category
            for task in tasks_with_category:
                task.category = new_category
                db.session.commit()    
            return return_back()
        else:
            return_back()   

    def create_function(self):
        if 'Add' in self.input_split:

            index_of_add = self.input_split.index('Add')
            cat_name = self.input_split[1:index_of_add]
           
            self.category_name = cat_name

            return self.execute_add_function()


    def do_by_function(self):
        index_of_by = self.input_split.index('By')
        task_name = self.input_split[:index_of_by]
        by_name = self.input_split[index_of_by+1:]
        task_name = ' '.join(task_name)
        by_name = ' '.join(by_name)

        deadline = ManageDeadlines.check_date(by_name)
        new_task = Tasks(task=task_name, date=deadline, category = self.category_name)
        db.session.add(new_task)
        db.session.commit()
        return return_back()


    def add_task(self):
        if self.category_name is not None:
            task = Tasks(task=self.input, category=request.args.get('category'))
            db.session.add(task)
            db.session.commit()
            # redirecting back to the category from which request came
            return redirect(url_for('category.show_category', name=self.category_name))

        else:
        # save task to Tasks category -> Default
            print('else section')
            task = Tasks(task=self.input)
            db.session.add(task)
            db.session.commit()
            return self.execute_main_function()  

    def execute_show_function(self):
        if self.category_name is None:
            return redirect(url_for('dashboard.home_page'))
        elif self.input_split[1] == 'deadlines':
            return redirect(url_for('category.show_category', name=self.category_name, sort='deadlines'))
        elif self.input_split[1] == 'optional':
            return redirect(url_for('category.show_category', name=self.category_name, sort='optional'))
        elif self.input_split[1] == 'list':
            return redirect(url_for('show_deadlines', name=self.category_name))
        else:
            return redirect(url_for('dashboard.home_page'))
    

    def execute_add_function(self):
        add_index = self.input_split.index('Add')
        tasks = self.input_split[add_index+1:]
        tasks = " ".join(tasks).split(',')
        print(self.category_name)
        for task in tasks:
            new_task = Tasks(task=task, category=self.category_name[0])
            db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('category.show_category', name=self.category_name))