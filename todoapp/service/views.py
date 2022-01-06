from . import service
from todoapp.some_func import return_back
from .logic import  delete_task, undo_task, complete_task
from flask import request
from todoapp.terminal_manager import terminal_manager


@service.route('/completed')
def completed():
    complete_task()
    return return_back()


@service.route('/undo')
def undo():
    undo_task()
    return return_back()


@service.route('/delete')
def delete():
    delete_task()
    return return_back()


@service.route('/terminal', methods=['POST'])
def terminal():
    users_input = request.form.get('add')
    return terminal_manager(users_input)
