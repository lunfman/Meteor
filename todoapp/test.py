from datetime import date, datetime, timedelta

def calculate_deadline(deadline):
    
    '''
    this function calculates how many days left till deadline
    and return a string with delta of days
    if one day left it return word like tomorrow.
    soon will add more words if needed
    '''
   
    # creating data object from deadline argument to calculate two date objs
    # after createing date objs call method date() because date.today is a date!!!
    deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    delta = deadline - date.today()

    delta = int(delta.days)

    if delta == 1:
        return 'tomorrow'
    elif delta < 0:
        return deadline
    else:
        return f'{delta} days'

#print(calculate_deadline('2021-12-05'))

# def in_command(input):
#     deadline = date.today() + timedelta(days=input)
#     print(deadline)
x