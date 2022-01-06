from todoapp.db_actions import DbActions, DashboardQueries
from flask import render_template

def get_categories_objs():
    categories = DbActions.get_all_categories_with_show()
    return categories

def get_categories():
    categories = get_categories_objs()
    categories_names = [category.name for category in categories]
    return categories_names
    # categories data -> key category:name and after {} -> {cat_name:{cat_data:}}


def create_categories_data(): 
    cat_data = {}  
    for category in get_categories_objs():
    # new_dict for storeing extracted data
        query = DashboardQueries(category.id)
        new_dict = {}
        
        by_today = query.count_by_today_category_tasks()
        new_dict['today'] = by_today
        
        by_tomorrow = query.count_by_tomorrow_category_tasks()
        new_dict['tomorrow'] = by_tomorrow
        
        tasks_number = query.count_category_tasks()
        new_dict['tasks'] = tasks_number
        
        tasks_comp_number = query.count_category_completed_tasks()
        new_dict['completed'] = tasks_comp_number

        expired = query.count_category_expired_tasks()
        new_dict['expired'] = expired

        no_deadlines = query.count_category_optional_tasks()
        new_dict['ordinary'] = no_deadlines

        # saveing extracted data to cat_data with category name as key
        cat_data[category.name] = new_dict

    return cat_data

# nameing!
def return_dashboard_logic():
    categories_names = get_categories()
    cat_data = create_categories_data()
  
    return render_template('index.html', categories=categories_names, data=cat_data)  