from . import dashboard
from todoapp.models import Tasks, Category
from datetime import date, timedelta
from flask import render_template
from todoapp import db
from todoapp.db_actions import DashboardQueries, DbActions
from .logic import get_categories, create_categories_data

@dashboard.route('/')
def home_page():

    categories_names = get_categories()
    cat_data = create_categories_data()
  
    return render_template('index.html', categories=categories_names, data=cat_data)
