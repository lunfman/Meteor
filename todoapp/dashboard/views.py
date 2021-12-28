from . import dashboard
from todoapp.models import Tasks
from datetime import date, timedelta
from flask import render_template
from todoapp import db

@dashboard.route('/')
def home_page():
    try:
        # categories names
        categories = (Tasks.query.distinct(Tasks.category).group_by(Tasks.category))
        # categories data -> key category:name and after {} -> {cat_name:{cat_data:}}
        cat_data = {}
   
        for category in categories:
            # new_dict for storeing extracted data
            new_dict = {}
            by_today =  Tasks.query.filter(Tasks.category == category.category, Tasks.date == date.today()).count()
            #print(f'By today {by_today}')
            # dates for tomorrow
            new_dict['today'] = by_today
            by_tomorrow = Tasks.query.filter(Tasks.category == category.category, Tasks.date == date.today() + timedelta(days=1)).count()
            #print(f'By tomorrow {by_tomorrow}')
            # tasks in category
            new_dict['tomorrow'] = by_tomorrow
            # total tasks
            tasks_number = Tasks.query.filter(Tasks.category == category.category).count()
            #print(f'Number of tasks {tasks_number}')
            new_dict['tasks'] = tasks_number
            # completed tasks in category
            tasks_comp_number = Tasks.query.filter(Tasks.category == category.category, Tasks.completed == True).count()
            #print(f'Number of completed tasks {tasks_comp_number}')
            new_dict['completed'] = tasks_comp_number
            # expired tasks
            expired =  Tasks.query.filter(Tasks.category == category.category, Tasks.date != '' ,Tasks.date < date.today()).count()
            #print(f'expired : {expired}')
            new_dict['expired'] = expired
            # not completed and without deadlines
            no_deadlines = Tasks.query.filter(Tasks.category == category.category, Tasks.date == '', Tasks.completed == False).count()
            #print(f'Tasks without deadline and not completed: {no_deadlines}')
            new_dict['ordinary'] = no_deadlines
            # saveing extracted data to cat_data with category name as key
            cat_data[category.category] = new_dict
        #print(cat_data)

    except:
        db.create_all()
        db.session.commit()
        cat_data = {}
        categories = []
    return render_template('index.html', categories=categories, data=cat_data)
