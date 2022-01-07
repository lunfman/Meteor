from . import category
from .logic import make_category_show, make_show_deadline

@category.route('/category/<name>')
def show_category(name):
    return make_category_show(name)

@category.route('/category/<name>/list')
def show_deadlines(name):
    return make_show_deadline(name)