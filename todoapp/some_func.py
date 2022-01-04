from flask import request, redirect, url_for
# TODO rename some_func to routes or something.
def return_back():
    """
    return_back function checks if request made from category tab ('/category/name') or from main menu ('/')
    if made from category -> redirect back to this category
    category value located in templates/category.html
    href={{url_for('completed', id=todo.id, category=category_name)}}
    """
    if request.args.get('category') is not None:
        # url_for takes name as an argument because show_category route = /category/<name>
        return redirect(url_for('category.show_category', name=request.args.get('category')))
    return redirect(url_for('dashboard.home_page'))
