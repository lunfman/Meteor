from . import category
from .logic import return_category_show, return_show_deadline

@category.route('/category/<name>')
def show_category(name):
    return return_category_show(name)

@category.route('/category/<name>/list')
def show_deadlines(name):
    return return_show_deadline(name)