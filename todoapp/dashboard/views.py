from . import dashboard
from todoapp.models import Tasks, Category
from datetime import date, timedelta
from flask import render_template
from todoapp import db

@dashboard.route('/')
def home_page():
    # category = Category.query.first()
    # print(category.tasks.task)
    #db.create_all()
    # new = Category(name='tasks')
    # db.session.add(new)
    # db.session.commit()
    # categories names
    categories = Category.query.filter(Category.show == True).all()
    categories_names = [category.name for category in categories]
    # categories data -> key category:name and after {} -> {cat_name:{cat_data:}}
    cat_data = {}

    for category in categories:
    # new_dict for storeing extracted data
        query = Tasks.query.filter(Tasks.category_id == category.id)
        new_dict = {}
        by_today =  query.filter(Tasks.date == date.today()).count()
        #print(f'By today {by_today}')
        # dates for tomorrow
        new_dict['today'] = by_today
        by_tomorrow = query.filter(Tasks.date == date.today() + timedelta(days=1)).count()
        #print(f'By tomorrow {by_tomorrow}')
        # tasks in category
        new_dict['tomorrow'] = by_tomorrow
        # total tasks
        tasks_number = query.count()
        #print(f'Number of tasks {tasks_number}')
        new_dict['tasks'] = tasks_number
        # completed tasks in category
        tasks_comp_number = query.filter(Tasks.completed == True).count()
        #print(f'Number of completed tasks {tasks_comp_number}')
        new_dict['completed'] = tasks_comp_number
        # expired tasks
        expired =  query.filter(Tasks.date != '' ,Tasks.date < date.today()).count()
        #print(f'expired : {expired}')
        new_dict['expired'] = expired
        # not completed and without deadlines
        no_deadlines = query.filter(Tasks.date == '', Tasks.completed == False).count()
        #print(f'Tasks without deadline and not completed: {no_deadlines}')
        new_dict['ordinary'] = no_deadlines
        # saveing extracted data to cat_data with category name as key
        cat_data[category.name] = new_dict
    print(cat_data)
    return render_template('index.html', categories=categories_names, data=cat_data)

        #print('here one more time')
        #tasks = Category(name='tasks')
        # db.create_all()
        # #db.session.add(tasks)
        # db.session.commit()
        # cat_data = {}
        # categories = []
        #return render_template('index.html', categories=categories_names, data=cat_data)
