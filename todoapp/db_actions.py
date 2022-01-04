from . import db
from .models import Category, Tasks
from datetime import date, timedelta

class DbActions:
    # Queries

    # rename this it is more likely if category None it is has name tasks..
    def get_current_category_obj(category_name):
        if category_name is None:
            return DbActions.get_category('tasks')
        return DbActions.get_category(category_name)
    

    def get_category(category_name):
        category_obj = Category.query.filter_by(name=category_name).first()       
        return category_obj
   

    def get_all_categories_with_show():
        return Category.query.filter(Category.show == True).all()        


    def get_unfinished_category_task(category_id):
        unfinished_category_task = Tasks.query.filter(Tasks.category_id == category_id,
            Tasks.completed == False).first()
        return unfinished_category_task
    
    def get_task_by_id(task_id):
        return Tasks.query.get(task_id)

    


         
# Actions

    def create_task(name, category):
        task = Tasks(task=name, category=category)
        DbActions.save(task)
        return 
        
   
    def save(obj):
        db.session.add(obj)
        db.session.commit()
        return

    def delete_obj(obj):
        db.session.delete(obj)
        db.session.commit()          

    def create_category(category_name):
        new_category = Category(name=category_name)
        DbActions.save(new_category)
        return



class DashboardQueries:

    def __init__(self, cat_id):
        self.cat_id = cat_id
        self.query = Tasks.query.filter(Tasks.category_id == self.cat_id)

    def count_by_today_category_tasks(self):
        by_today = Tasks.query.filter\
            (Tasks.category_id == self.cat_id,\
            Tasks.date == date.today())\
            .count()
        return by_today

    def count_by_tomorrow_category_tasks(self):
        query = Tasks.query.filter(Tasks.category_id == self.cat_id)

        by_tomorrow = query.filter\
            (Tasks.date == date.today() + timedelta(days=1))\
            .count()

        return by_tomorrow

    def count_category_tasks(self):
        query = Tasks.query.filter(Tasks.category_id == self.cat_id)
        tasks_sum = query.count()
        return tasks_sum

    def count_category_completed_tasks(self):
        query = Tasks.query.filter(Tasks.category_id == self.cat_id)
        completed_sum = query.filter(Tasks.completed == True).count()
        return completed_sum

    
    def count_category_expired_tasks(self):
        query = Tasks.query.filter(Tasks.category_id == self.cat_id)
        expired_sum = query.filter\
            (Tasks.date != '' ,Tasks.date < date.today()).count()
        return expired_sum

    def count_category_optional_tasks(self):
        query = Tasks.query.filter(Tasks.category_id == self.cat_id)
        optional_sum = query.filter\
            (Tasks.date == '', Tasks.completed == False).count()
        return optional_sum