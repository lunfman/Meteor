from flask import request
from todoapp.db_actions import DbActions

# undo_task and complete_task almost identical code.
# But i am not going to create function for them which 
# takes boolean as an argument!

def undo_task():
    task_obj = get_task_obj()
    task_obj.completed = False
    DbActions.save()
    return

def complete_task():
    task_obj = get_task_obj()
    task_obj.completed = True
    DbActions.save()
    return


def get_task_obj():
    task_id = request.args.get('id')
    task_obj = DbActions.get_task_by_id(task_id)
    return task_obj

def delete_task():
    task_obj = get_task_obj()
    DbActions.delete_obj(task_obj)
    return    