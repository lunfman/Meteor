from datetime import date, timedelta
# creating a deadline class to check different deadline scenarios


class Deadline:
    '''
    -Deadline class allow to track deadlines by using methods
    -Class methods always return a date

    -Init creates next vars:
        today - current day
        cur_year - current year
        cur_month - current month
        latest - stores latest value after method use in the class

        dates -> dictionary has next keys: tomorrow, next week, next month  
            -> every key has a logical date value to every key

        month_list -> main goal is to use it in creation of a self.month dict

        self.motnhs -> dict which is using if user want 
            to complete something By month


    -Methods

        - check_deadlines takes as an argument string. This method checks
        if the string in the dates dict if so returns value of the key

        -cur_month_deadline takes as an argument string. after try 
        to convert to string if impossible return none if everythin is okay
        return a date with the current year, month and provided day

        -by_month takes as an argument string if the string in months dict return value of the key

        -by_month_and_day takes two arguments month and day -> at the begining this method call by_month method
        and after replaces the day from date received from this method.
    '''


    def __init__(self, input):

        self.today = date.today()
        self.cur_year = self.today.year
        self.cur_month = self.today.month
        
        # stores latest value after method exe
        self.latest = ''
        
        self.dates = {
            'tomorrow': self.today + timedelta(days=1),
            'next week': self.today + timedelta(days=7),
            'next month': self.today + timedelta(days=30),
        }
        
        # month_list allow to create moths dict
        self.month_list = ['january', 'february', 'march', 'april', 
            'may', 'june', 'july', 'august','september', 'october',
            'november', 'december']
        
       # creating dict from month_list
        self.months = {self.month_list[num]: date(self.cur_year, num + 1, 1)
         for num in range(len(self.month_list))}

        self.input = input
        self.month = ''
        self.day = ''
       

    def check_deadline(self):
        # this method checks if user typed keywords like 'tomorrow' , 'next week'
        # creating deadline by using dates dict 
        if self.input in self.dates:
            self.latest = self.dates[self.input]
            return self.latest
        return None


    def cur_month_deadline(self):
        # method checks if user typed number as an argument
        # return -> Current month year and input as a day
        try:
            self.latest = self.today.replace(day=int(self.input))
            return self.latest
        except:
            return None
        

    def by_month(self):
        # check current month if december or the current month > than wanted => new year
        # else return value from self.months
        input = self.input.lower()
        if input in self.months:
            # if now is december it means next month will be in the new year
            # if now is october and do by february -> new year
            # getting index of the input month from self.month_list
            
            index_of_input_month = self.month_list.index(input)
            
            # do_by-> users month = index + 1
            # why? because month_list stores all 12 motnhs and we got the index of the users month
            # it means than if add 1 to this number we get a month number!
            do_by = index_of_input_month + 1

            if self.cur_month == 12 or self.cur_month > do_by:
                # changeing year in value of months dict
                self.latest = self.months[input].replace(year=self.cur_year + 1)
                return self.latest
            else:
                # if not december or sum of two months =!
                self.latest = self.months[input]
                return self.latest
        return None


    def in_command(self):
        # in_command method return a date after calculateing delta of todays and users desired day
        # in_command take one argument -> input which should be a integer or str convertable to integer
        # in command can tak up to 90 if more it will be a mess! In 1000, or in 10000000000 days
        # 90 looks okay because it is really hard to plan task this way
        # Try except to check if input is a digit  and not 'In 90' or some kind of
        try:
            input = int(self.input)
            if input > 90:
                return None
            else:
                deadline = self.today + timedelta(days=input)
                return deadline
        except TypeError:
            return None

        except ValueError:
            return None


    def by_month_and_day(self):
        # this method create date by using month and day
        try:
            input = self.input.split()
            self.month = input[1]
            self.day = input[0]
            self.input = self.month
            # using by month method to get date
            date = self.by_month()
            # after replace day with wanted one and return
            self.latest = date.replace(day=int(self.day))
            return self.latest
        except:
            return None

class ManageDeadlines(Deadline):
    '''
    This method allows to organize deadline validation in this app
    It init Deadline class and after checks for every possible scenarios of users input
    Return deadline.latest -> because all methods in Deadline class checks if they valid and 
    return none or date

    If not none -> return self.deadline.latest
    '''

    def check_date(self):
        
        # split users_input by 'By' and selecting dead line value and use strip 
        # to get rid of eny spaces and make it lower
        # and checking if by By was typed
        #try:
        self.input = self.input.strip().lower()
            #self.task = input.split('By')[0].strip().lower()
        # except IndexError:
        #     # By was not typed -> wrong format
        #     return None

        # this section validates dates by using deadline class methods
        # if return is not none going to return latest functions return value
        
        if self.check_deadline():
            return self.latest
        elif self.cur_month_deadline():
            return self.latest
        elif self.by_month():
            return self.latest
        else:
            # here we need to do split again because the last method takes two arguments
            # month after split has index 1
            # day has 0
            try:
                # if user type 'By 3 march and' we will get date anyway nice
                #self.input = self.month
                if self.by_month_and_day():
                    return self.latest
            except:
                return None

# input = '  3 May'
# deadline = ManageDeadlines(input)
# deadline.check_date()
