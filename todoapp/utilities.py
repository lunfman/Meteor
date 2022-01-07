from datetime import datetime, date

class ExtractCommand:


    def extract_single_command_value(input):
        # Comand .......
        value = input.split()[1:]
        return ' '.join(value)


    def extract_middle_value(input, seperator):
        # Add ..middlevalue.. By...
        # seperator value should be defined to use this method
        input_split = input.split()
        index_of_seperator = input_split.index(seperator)
        value = input_split[1:index_of_seperator]
        value = ' '.join(value)
        return value


    def extract_after_value(input, seperator):
        # Comand .... Command 2 ....after value....
        # Comand some values Seperator after seperator values
        input_split = input.split()
        index_of_seperator = input_split.index(seperator)
        value = input_split[index_of_seperator+1:]
        value = ' '.join(value)
        return value

# utility
class DateOutput:
    def __init__(self, deadline_date):
        self.deadline = datetime.strptime(deadline_date, '%Y-%m-%d').date()
        delta = self.deadline - date.today()
        self.delta = int(delta.days)


    def base_modify_date(self):
        if self.delta == 1:
            return 'tomorrow'
        elif self.delta == 0:
            return 'today'


    def modify_deadline_date(self):
        base = self.base_modify_date()
        if base:
            return base
        
        if self.delta < 0:
            return f'{self.deadline} !!!'
        else:
            return self.deadline


    def modify_category_date(self):
        base = self.base_modify_date()
        if base:
            return base

        if self.delta < 0:
            return 'Failed'
        else:
            return f'{self.delta} days'    