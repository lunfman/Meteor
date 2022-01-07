from . import category
from .logic import make_category_show, make_show_deadline
from flask import request

@category.route('/category/<name>')
def show_category(name):
    print(request.args.get('sort'))
    return make_category_show(name)

@category.route('/category/<name>/list')
def show_deadlines(name):
    return make_show_deadline(name)