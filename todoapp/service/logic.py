from flask import request
from todoapp import db
from todoapp.models import Tasks

# TODO refactor this function do not like that it takes boolean as an argument
def is_task_completed(boolean):

    # function takes boolean as argument
    # function used in completed and undo section
    
    # getting task id from id arg -> id arg comes from template check 
    # return_back function for more info
    task_id = request.args.get('id')
    
    # looking for the task in db by id
    completed_task = Tasks.query.get(task_id)
    
    # changing tasks completed to true
    completed_task.completed = boolean
    
    # saving
    db.session.commit()