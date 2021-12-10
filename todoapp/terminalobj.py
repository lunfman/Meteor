
from os import name


class Terminal:
    '''
    terminal class works with command objects and returns 
    a command function with extracted info for this command
    It means that every function call back from command obj also will get extracted value

    Also this also return output to the function if it was executed
    so the function should have one parameter not more!
    '''
    def __init__(self, commands=[]):
        # self commands accept only command objs
        self.commands = commands
        # commands name from command obj
        self.commands_names = [command.name for command in self.commands]
        # commands_dict stores order true commands because they must be execute after
        self.commands_dict = {}

    
    def get_command(self, input):
        # get command method takes input as an argument and creates two lists
        # one list which is going to store all found commands
        # second list which is going to store command placement
       
        self.cur_commands = []
        self.command_place = []
        
        # if something present in the string before command was found
        # will be stored here
        self.before_command = []
        
        # creating var for storing input in the class
        # private property !!!
        self._input = input

        # iterate through input to get commands and command places
        for index, word in enumerate(input.split()):
            if word in self.commands_names:
                # adding to the list if word in commands_names
                self.cur_commands.append(word)
                self.command_place.append(index)
            else:
                # if command not found at the begining going to store data 
                # in before_command list
                if len(self.cur_commands) == 0:
                    self.before_command.append(word)
        return self
    
    
    def add_command(self, new):
        # this method add command in the commands list
        self.commands.append(new)
        return self


    def command_extractor(self):
        # split the input data
        # if multiple same commands was used it will replace it with the latest value!!!
        clean_data = self._input.split()

        for index, command in enumerate(self.cur_commands):
            # iterate trough every command in cur commands
           
            # getting command obj index by getting index of command name from commands_name
            # creating in order from command objs so name index = to obj index
            command_index = self.commands_names.index(command)
            # selecting command obj
            current_command = self.commands[command_index]
           
            # getting commands seperator
            command_separator = current_command.separator
            
            # checking if next command exists in the order
            # if index +1 = len => last command
            # checking if this is the last command 
            if index + 1 == len(self.cur_commands):
                # cur_place used after for slicing the clean data list
                # thats why it has + 1 after
                # getting the place of the command
                cur_place = self.command_place[index] + 1
                # if it is last commnad -> next_place is none so i added = ''
                next_place = ''
            else:
                # next command exitsts
                # cur place = place + 1 cause of slicing
                cur_place = self.command_place[index] + 1

                # and next place equal to its place number
                next_place = self.command_place[index + 1]

            # checking what params command obj has and do actions

            # checking if commands seperator is spaces and next places exists
            if command_separator == ' ' and next_place != '':
                # value = slice of cur_place command and next command place
                # value locates in the middle of two
                value = clean_data[cur_place : next_place]
                value = [value.strip() for value in value]
                # if command order attribute is True
                # this command can be combined
                if current_command.order:
                    # if command can be combined save to dict for after work
                    # adding to dict
                    # print('command combo found')
                    # print('going to use dict constructor after')
                    self.commands_dict[command] = value
                else:
                    # if command can not be combined execute it immediately 
                    return self.commands[command_index].task(value)
            
            # checking if commands separator is space and next places do not exists
            elif command_separator == ' ' and next_place == '':
                value = clean_data[cur_place:]
                value = [value.strip() for value in value]
                # if index >1 it means we deal with combo commands
                if index > 1:
                    self.commands_dict[command] = value
                    # print('command combo found')
                    # print('going to use dict constructor after')
                else:
                    return self.commands[command_index].task(value)
           
            # checking if seperator not spaces and next places exist
            elif command_separator != ' ' and next_place !='':
                #print('here here 3')
                cur_values = ' '.join(clean_data[cur_place : next_place]).split(command_separator)
                #self.command_dict[command] = cur_values
                cur_values = [value.strip() for value in cur_values]
                if current_command.order:
                    # if command can be combined save to dict for after work
                    self.commands_dict[command] = cur_values
                else:
                    return self.commands[command_index].task(cur_values)
            else:
                #print('here here 4')
                # command_seperator != spaces and next places do not exist
                cur_values = ' '.join(clean_data[cur_place:]).split(command_separator)
                cur_values = [value.strip() for value in cur_values]
                #self.command_dict[command] = cur_values
                if index > 0:
                    # print('command combo found')
                    # print('going to use dict constructor after')
                    self.commands_dict[command] = cur_values
                else:
                    return self.commands[command_index].task(cur_values)
        # if checked all commands and did not exe anything ->
        # exe from the list and use method for this action
        return self.dict_extractor()


    def dict_extractor(self):
        # iterate through dict and exe function of the comand obj with value
        counter = 0
        for key, value in self.commands_dict.items():
            counter += 1
            # getting index of command obj by using comands name list
            command_obj_index = self.commands_names.index(key)
            # selecting current obj
            cur_command = self.commands[command_obj_index]
            
            if counter == len(self.commands_dict):
                # if it is the last function to extract it will return this function!
                return cur_command.task(value)
            # exe objects value
            else:
                cur_command.task(value)




    def update_names(self):
        self.commands_names = [command.name for command in self.commands]
        return self


    def before_command_string(self):
        return ' '.join(self.before_command)


    def check_for_commands(self):
        # method checks if cur_commands empty or not
        if self.cur_commands == []:
            return False
        else:
             return True

class Command:
    # blue print for creating command object
    # not his obj do not have any methods

    def __init__(self, name, function, separator = ' ', order = False):
        self.name = name
        self.separator = separator
        self.task = function
        # order property specify if it possible to combine commands
        self.order = order

# input = 'Create new Add test1, test2, test3 test'
# cur_com = ['Create', 'Add']
# cur_place = [0,2]
# cur_split = input.split(' ')
# print(cur_split[1:2])
# print(' '.join(cur_split[3:]).split(','))

# terminal = Terminal()

# def open_command_fun(input):
#     print('open', input)

# def rename_command_fun(input):
#     print('rename values', input)

# def add_command_fun(input):
#     print('add command', input)

# def create_command_fun(input):
#     print('command found', input)

# Creating commands
# open_command = Command('Open', open_command_fun)
# rename_command = Command(name='Rename', separator='To', function=rename_command_fun)
# add_command_ = Command(name = 'Add', separator=',', function=add_command_fun, order=True)
# create_command = Command(name = 'Create', order= True, function= create_command_fun)
# create_command = Command(name = 'By', order= True, function= create_command_fun)

# terminal.add_command(open_command).add_command(rename_command).add_command(add_command_)
# terminal.add_command(create_command).update_names()
# terminal.get_command('Open task').command_extractor()
# #terminal.get_command('Rename old category To new category').command_extractor()
# #terminal.get_command('Rename old To new Open task').command_extractor()
# #terminal.get_command('Create new cat Add task, black friday').command_extractor()
# terminal.get_command('task By tomorrow').command_extractor()