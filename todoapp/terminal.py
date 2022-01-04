from flask import request


class Terminal:

    def __init__(self, input):
        self.commands = {}

        self.input = input
        self.input_split = self.input.split()

        self.seperator = ''

        self.category_name = request.args.get('category')


    def validate_input(self):
        # check if input has data or not
        if self.input.strip() == '':
            return False
        return True


    def find_command(self):
        for value in self.input_split:
            if value in self.commands.keys():
                command_obj = self.commands[value]
                # init command obj
                command = command_obj(self.input)
                # return run_command method of the command
                return command.run_command()
        return 'command not found'


    def execute_command(self):

        if self.validate_input():
            return self.find_command()
        return 'not valid input'


    def add_command(self, command_obj):

        command_name = command_obj.name
        self.commands[command_name] = command_obj
        return  
