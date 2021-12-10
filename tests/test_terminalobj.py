import unittest
from todoapp import terminalobj


class testTerminalObj(unittest.TestCase):

    def setUp(self):
        self.terminal = terminalobj.Terminal()
        self.command_creator = terminalobj.Command
        #def command_function(input):
         #   return input
        #self.open_command = self.command_creator('name', command_function)
    

    def test_command_obj(self):
        def command_function(input):
            return input

        # creating categories
        open_command = self.command_creator('Open', command_function)
        rename_command = self.command_creator(name='Rename', separator='To', function=command_function)
        create_command = self.command_creator(name = 'Create', function=command_function, order=True)
        add_command = self.command_creator(name = 'Add', function=command_function, order=True, separator=',')
        # adding to terminal       
        self.terminal.add_command(open_command).add_command(rename_command)
        self.terminal.add_command(add_command).add_command(create_command).update_names()
       
        self.assertEqual(self.terminal.get_command('Open category').command_extractor()
            , ['category'])

        self.assertEqual(self.terminal.get_command('Open category with long name').command_extractor()
            , ['category', 'with', 'long', 'name'])

        self.assertEqual(self.terminal.get_command('Open category Rename').command_extractor()
            , ['category'])  


        self.assertEqual(self.terminal.get_command('Rename category To new').command_extractor(),
            ['category', 'new'])

        self.assertEqual(self.terminal.get_command('Rename category long To new long').command_extractor(),
            ['category long', 'new long'])

        self.assertEqual(self.terminal.get_command('Rename category long To new long Open category').command_extractor(),
            ['category long', 'new long'])


        self.assertEqual(self.terminal.get_command('Create category Add task').command_extractor(), self.terminal.dict_extractor())
        self.assertEqual(self.terminal.get_command('Create category').command_extractor(), ['category'])
        self.assertEqual(self.terminal.get_command('Add task1, task2, task3 and 4').command_extractor(),
            ['task1', 'task2', 'task3 and 4'])
        self.assertEqual(self.terminal.get_command('Create category long').command_extractor(), ['category', 'long'])
        self.assertEqual(self.terminal.get_command('task1 and task2').before_command, ['task1', 'and', 'task2'])
        self.assertEqual(self.terminal.get_command('task1 and task2').before_command_string(), 'task1 and task2')
        