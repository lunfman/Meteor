from datetime import datetime, date

def date_output(deadline):
    deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    delta = deadline - date.today()

    delta = int(delta.days)

    if delta == 0:
        return 'Today'
    elif delta == 1:
        return 'Tomorrow'
    elif delta < 0:
        return f'{deadline} !!!'
    else:
        return deadline

def calculate_deadline(deadline):
    
    '''
    this function calculates how many days left till deadline
    and return a string with delta of days
    if one day left it return word like tomorrow.
    soon will add more words if needed
    '''

    # checking if deadline empty or note
    if deadline == '':
        return '-'
   
    # creating data object from deadline argument to calculate two date objs
    # after createing date objs call method date() because date.today is a date!!!
    deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    delta = deadline - date.today()

    delta = int(delta.days)

    if delta == 1:
        return 'tomorrow'
    elif delta == 0:
        return 'today'
    elif delta < 0:
        return 'Failed'
    else:
        return f'{delta} days'