from datetime import date
from flask import redirect, url_for, request
from .models import Category, Tasks
from .date_manage import ManageDeadlines
from .some_func import return_back
from . import db


class Terminal:
    def __init__(self, input):
        # Create-Add-BY not By-Add-Create order !!!!
        # order mothers !
        # Commands Create category Add tasks By date
        # Add tasks By date
        self.commands = {
            'Open': self.execute_open_function,
            'Rename': self.execute_rename_function,
            'Create': self.execute_create_function,
            'Main': self.execute_main_function,
            'Show': self.execute_show_function,
            'Add': self.execute_add_function,
            'By': self.execute_by_function,
            'Help': self.execute_help_function,
            'Hide': self.execute_hide_function,
            'Reveal': self.execute_reveal_function,
            'Delete': self.execute_delete_category_function,
            'Migrate': self.execute_migrate_function}

        self.input = input
        self.input_split = self.input.split()

        self.seperator = ''

        # category for redirect and saveing tasks
        # default category tasks in none by default! if request from dashboard
        self.category_name = request.args.get('category')


    def validate_input(self):
        # check if input has data or not
        if self.input.strip() == '':
            return False
        return True

# execute_command
    def check_input(self):
        for key in self.commands.keys():
            if key in self.input:
                return self.commands.get(key)()
        
        return self.add_task()
    

    def extract_single_command_value(self):
        # Comand .......
        value = self.input_split[1:]
        return ' '.join(value)


    def extract_middle_value(self):
        # Add ..middlevalue.. By...
        # seperator value should be defined to use this method
        self.index_of_seperator = self.input_split.index(self.seperator)
        value = self.input_split[1:self.index_of_seperator]
        value = ' '.join(value)
        return value

    def extract_after_value(self):
        # Comand .... Command 2 ....after value....
        # Comand some values Seperator after seperator values
        self.index_of_seperator = self.input_split.index(self.seperator)
        value = self.input_split[self.index_of_seperator+1:]
        value = ' '.join(value)
        return value

    
    def get_current_category_obj(self):
        if self.category_name is None:
            return Category.query.filter_by(name='tasks').first()
        return Category.query.filter_by(name=self.category_name).first()
        

    def execute_main_function(self):
        return redirect(url_for('dashboard.home_page'))


    def execute_open_function(self):
        category_name = self.extract_single_command_value()
        return redirect(url_for('category.show_category', name = category_name.lower()))


    def execute_rename_function(self):

        if 'To' in self.input_split:
            self.seperator = 'To'
            old_category = self.extract_middle_value()
            new_category = self.extract_after_value()

            if new_category.strip() == '':
                return return_back()

            cur_category = Category.query.filter_by(name=old_category).first()

            if cur_category:
                cur_category.name = new_category
                db.session.commit()
                return return_back()
            return return_back()

        else:
            return return_back()   
    
    def execute_create_function(self):
        
        def create_new_category(category_name):

            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()

        def validate_category(category_name):

            new_category = Category.query.filter_by(name=category_name).first()
            
            if new_category:
               return return_back()
            # add flash messages after
            create_new_category(category_name)
            return
            
        if 'Add' in self.input_split:
            self.seperator = 'Add'
            # index_of_add = self.input_split.index('Add')
            # cat_name = self.input_split[1:index_of_add]
            self.category_name = self.extract_middle_value()
            
            validate_category(self.category_name)

            # add self seperator so the execute_add_functions knows
            #  it comes from Create
            

            return self.execute_add_function()

        else:
            category_name = self.extract_single_command_value()

            validate_category(category_name)

            return return_back()

    # execute_by_function
    def execute_by_function(self):
        
        index_of_by = self.input_split.index('By')
        task_name = self.input_split[:index_of_by]
        by_name = self.input_split[index_of_by+1:]
        task_name = ' '.join(task_name)
        by_name = ' '.join(by_name)

        category = self.get_current_category_obj()    
        deadline = ManageDeadlines(by_name).check_date()
        self.task = Tasks(task=task_name, date=deadline, category = category)

        self.save_task()
        return return_back()


    def create_task(self):

        self.category = self.get_current_category_obj()
        self.task = Tasks(task=self.input, category=self.category)
        return


    def save_task(self):

        db.session.add(self.task)
        db.session.commit()
        return
        

    def add_task(self):

        if not self.validate_input():
            return return_back()
        
        self.create_task()
        self.save_task()
        return return_back()


    def execute_show_function(self):

        if self.category_name is None:
            return redirect(url_for('dashboard.home_page'))
        elif self.input_split[1] == 'deadlines':
            return redirect(url_for('category.show_category', name=self.category_name,
                sort='deadlines'))
        elif self.input_split[1] == 'optional':
            return redirect(url_for('category.show_category', name=self.category_name, sort='optional'))
        elif self.input_split[1] == 'list':
            return redirect(url_for('category.show_deadlines', name=self.category_name))
        else:
            return redirect(url_for('dashboard.home_page'))
    

    def find_tasks(self):
       # if self.seperator Add was used in create category
        # Create category name Add .....
        if self.seperator == 'Add':
            if 'By' in self.input_split:
                # Create .... Add... By..
                # index of add was used before so it saved
                add_index = self.index_of_seperator
                by_index = self.input_split.index('By')
                tasks = self.input_split[add_index+1:by_index]
                tasks = ' '.join(tasks)
                return tasks
            # Create....Ad...
            else:
                return self.extract_after_value()

        elif 'By' in self.input_split:
            self.seperator = 'By'
            # Add ..... By ...
            return self.extract_middle_value()

        else:
            # Add ......
            return self.extract_single_command_value()

    def execute_add_function(self):

        tasks = self.find_tasks().split(',')

        current_category = self.get_current_category_obj()

        if 'By' in self.input_split:
            self.seperator = 'By'
            by_name = self.extract_after_value()
            deadline = ManageDeadlines(by_name).check_date()

            for task in tasks:
                # create by add_tasks and save method?? or not ..
                new_task = Tasks(task=task, category=current_category, date=deadline)
                db.session.add(new_task)
        else:
            for task in tasks:
                # create by add_tasks and save method?? or not ..
                new_task = Tasks(task=task, category=current_category)
                db.session.add(new_task)
        
        db.session.commit()
        return redirect(url_for('category.show_category', name=self.category_name))


    def execute_help_function(self):

        return redirect(url_for('help.help'))


    def hide_reveal_functionality(self, boolean):

        category_name = self.extract_single_command_value()
        category = Category.query.filter_by(name=category_name).first()
        category.show = boolean
        db.session.commit()
        return redirect(url_for('dashboard.home_page'))


    def execute_hide_function(self):

        return self.hide_reveal_functionality(False)


    def execute_reveal_function(self):

        return self.hide_reveal_functionality(True)


    def execute_delete_category_function(self):
        # can not delete not empty category!
        # delete something -> extract_first_single command value
        category_name = self.extract_single_command_value()
        category = Category.query.filter_by(name=category_name).first()
        
        # if category do not exists return back
        if not category:
            return return_back()


        if len(category.tasks) > 0:
            # check if all task completed
            unfinished_tasks = Tasks.query.filter(Tasks.category_id == category.id,
                Tasks.completed == False).first()

            if not unfinished_tasks:
                print('delete category')
                db.session.delete(category)
                db.session.commit()
                return self.execute_main_function()
            else:
                print('send warning')
                return return_back()
        
        db.session.delete(category)
        db.session.commit()
        return self.execute_main_function()

    
    def execute_migrate_function(self):
        # migrate to category
        # Migrate category 1 To category 2
        # or Migrate category 1 -> to tasks
        self.seperator = 'To'
        category_1 = self.extract_middle_value()
        category_2 = self.extract_after_value()

        # just change category name to another?
        cat_1_obj = Category.query.filter_by(name=category_1).first()
        cat_2_obj = Category.query.filter_by(name=category_2).first()
        #cur_category.tasks()
        tasks =  cat_1_obj.tasks
        print(tasks)
        for task in tasks:
            task.category_id = cat_2_obj.id
            db.session.commit()
        
        return return_back()


# class Command:
#     pass