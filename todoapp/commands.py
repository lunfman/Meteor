# templates
from re import I
from flask import request, redirect, url_for
from .models import Tasks
from .db_actions import DbActions
from .utilities import ExtractCommand
from . import db
from .some_func import return_back
from .date_manage import ManageDeadlines

# Templates
class Command:

    def __init__(self,input):
        self.input = input
        self.input_split = self.input.split()
        self.category_name = request.args.get('category')   


class HideRevealTemplate(Command):

    def __init__(self, input):
        super().__init__(input)
        category_name = ExtractCommand.extract_single_command_value(self.input)
        self.category = DbActions.get_category(category_name)

    def save_changes(self):
        db.session.commit()
        return redirect(url_for('dashboard.home_page'))    


class MiddleSeperatorCommand(Command):
    
    def __init__(self, input):
        super().__init__(input)

    # seperator should be in init?!
    def find_seperator_in_input(self):
        if 'To' in self.input_split:
            self.seperator = 'To'
            return True
        return False


    def extract_categories(self):
        self.old_category = ExtractCommand.extract_middle_value(self.input, self.seperator)
        self.new_category = ExtractCommand.extract_after_value(self.input, self.seperator)
        return


    def check_is_new_category_empty(self):
        if self.new_category.strip() == '':
            return True
        return False


# Commands
class OpenCommand(Command):
    # Open ......
    name = 'Open'
    def __init__(self, input):
        super().__init__(input)
    
    def run_command(self):
        category_name =  ExtractCommand.extract_single_command_value(self.input)
        return redirect(url_for('category.show_category', name = category_name.lower()))


class MainCommand(Command):
    # Main .....
    name = 'Main'
    def __init__(self, input):
        super().__init__(input)
    
    def run_command(self):
        return redirect(url_for('dashboard.home_page'))


class RenameCommand(MiddleSeperatorCommand):

    name = 'Rename'


    def __init__(self,input):
        super().__init__(input)


    def rename_category(self):
        if self.old_category_obj:
            self.old_category_obj.name = self.new_category
            db.session.commit()

    
    def rename_command(self):

        if self.find_seperator_in_input():
            self.extract_categories()
            
            if self.check_is_new_category_empty():
                return return_back()
            
            self.old_category_obj = DbActions.get_category(self.old_category)
            self.rename_category()
        
        return return_back()

    def run_command(self):
        return self.rename_command()       


class CreateCommand(Command):
    name = 'Create'


    def __init__(self,input):
        super().__init__(input)


    def validate_category(self):

        new_category = DbActions.get_category(self.category_name)
        # if category already exists return False Unique only!
        if new_category:
            return True
        # add flash messages after
        DbActions.create_category(self.category_name)
        return False
    

    def create_command(self):

        if 'Add' in self.input_split:
            self.category_name = ExtractCommand.extract_middle_value(self.input, 'Add')
            
            if self.validate_category():
                return return_back()

            LatestChanges.category = self.category_name
            add_command = AddCommand(self.input)
            return add_command.run_command()

        else:
            self.category_name = ExtractCommand.extract_single_command_value(self.input)

            if self.validate_category():
                return return_back()

            return return_back()    
    
    def run_command(self):
        return self.create_command()


class ByCommand(Command):
    # execute_by_function
    name = 'By'

    def __init__(self,input):
        super().__init__(input)

    def extract_values(self):
        index_of_by = self.input_split.index('By')
        task_name = self.input_split[:index_of_by]
        by_name = self.input_split[index_of_by+1:]
        self.task_name = ' '.join(task_name)
        self.by_name = ' '.join(by_name)


    def add_by_command(self):
        
        self.extract_values()
        
        category_name = request.args.get('category')
        category = DbActions.get_current_category_obj(category_name)    
        deadline = ManageDeadlines(self.by_name).check_date()
        task = Tasks(task=self.task_name, date=deadline, category = category)
        DbActions.save(task)

        return return_back()


    def run_command(self):
        return self.add_by_command()


class ShowCommand(Command):
    name = 'Show'
    def __init__(self, input):
        super().__init__(input)    

    def show_command(self):

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

    def run_command(self):
        return self.show_command()

class AddCommand(Command):

    name = 'Add'

    def __init__(self, input):
        super().__init__(input)

    def find_tasks(self):
        # if self.seperator Add was used in create category
        # Create category name Add .....
        if 'Create' in self.input_split:
            self.category_name = LatestChanges.category
            if 'By' in self.input_split:
                # Create .... Add... By..
                add_index = self.input_split.index('Add')
                by_index = self.input_split.index('By')
                tasks = self.input_split[add_index+1:by_index]
                tasks = ' '.join(tasks)
                return tasks
            # Create....Ad...
            else:
                return ExtractCommand.extract_after_value(self.input,'Add')

        elif 'By' in self.input_split:
            self.seperator = 'By'
            # Add ..... By ...
            return ExtractCommand.extract_middle_value(self.input, self.seperator)

        else:
            # Add ......
            return ExtractCommand.extract_single_command_value(self.input)

    def add_command(self):

        tasks = self.find_tasks().split(',')

        current_category = DbActions.get_current_category_obj(self.category_name)

        if 'By' in self.input_split:
            self.seperator = 'By'
            by_name = ExtractCommand.extract_after_value(self.input, self.seperator)
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

    def run_command(self):
        print('running add command')
        return self.add_command()


class HelpCommand(Command):
    name = 'Help'
    def __init__(self,input):
        super().__init__(input)

    def run_command(self):
        return redirect(url_for('help.help'))


class HideCommand(HideRevealTemplate):
    
    name = 'Hide'

    def __init__(self, input):
        super().__init__(input)
   
    def hide_command(self):
        self.category.show = False
        return self.save_changes()
    
    def run_command(self):
        return self.hide_command()

class RevealCommand(HideRevealTemplate):
    
    name = 'Reveal'

    def __init__(self, input):
        super().__init__(input)
    
    def reveal_command(self):
        self.category.show = True
        return self.save_changes()

    def run_command(self):
        return self.reveal_command()           


class DeleteCommand(Command):
    '''
    Can delete only empty category!
    '''
    name = 'Delete'


    def __init__(self, input):
        super().__init__(input)


    def get_category_obj(self):
        category_name = ExtractCommand.extract_single_command_value(self.input)
        self.category = DbActions.get_category(category_name)
    

    def delete_command(self):

        self.get_category_obj()

        if not self.category:
            return return_back()


        if len(self.category.tasks) > 0:
            # check if all task completed
            unfinished_category_task = DbActions.get_unfinished_category_task(self.category.id)

            if not unfinished_category_task:
                DbActions.delete_obj(self.category)
                return return_back()
            else:
                print('send warning')
                return return_back()
        
        
        DbActions.delete_obj(self.category)
        return return_back()

    def run_command(self):
        return self.delete_command()

class MigrateCommand(MiddleSeperatorCommand):
    '''
    migrate to category
    Migrate category 1 To category 2
    '''
    name = 'Migrate'

    def __init__(self, input):
        super().__init__(input)  


    def get_categories_objects(self):    
        self.cat_1_obj = DbActions.get_category(self.old_category)
        self.cat_2_obj = DbActions.get_category(self.new_category)

    def migrate_tasks(self):
        tasks =  self.cat_1_obj.tasks
        for task in tasks:
            task.category_id = self.cat_2_obj.id
            db.session.commit()        

    def migrate_command(self):

        if self.find_seperator_in_input():
            self.extract_categories()

            if self.check_is_new_category_empty():
                return return_back()

            self.get_categories_objects()
            self.migrate_tasks()
        
        return return_back()

    def run_command(self):
        return self.migrate_command()


class AddTask:
    # rename
    def save(name, category_name):
        category = DbActions.get_current_category_obj(category_name)
        DbActions.create_task(name, category) 


class LatestChanges:
    # class for information transit
    # now used for category to add command transit only!
    category = ''