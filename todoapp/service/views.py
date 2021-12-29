from . import service
from todoapp import db
from todoapp.some_func import return_back
from .logic import is_task_completed
from todoapp.models import Tasks
from flask import request
from todoapp.terminal import Terminal

@service.route('/completed')
def completed():
    is_task_completed(True)
    return return_back()

@service.route('/undo')
def undo():
    is_task_completed(False)
    return return_back()


@service.route('/delete')
def delete():

    # getting id from jinja template
    task_id = request.args.get('id')
    
    # looking for the task by id
    task_to_delete = Tasks.query.get(task_id)
    
    # deleting task from db
    db.session.delete(task_to_delete)
    
    # saving
    db.session.commit()
    return return_back()


@service.route('/terminal', methods=['POST'])
def terminal():
    users_input = request.form.get('add')
    return Terminal(users_input).check_input()

