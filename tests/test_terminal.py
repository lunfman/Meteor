import unittest
from todoapp import terminal
from freezegun import freeze_time
from datetime import date

class TestTerminal(unittest.TestCase):
   

    @freeze_time('2021-12-01')
    def setUp(self):
        # init terminal class
        self.terminal = terminal.Terminal()
    
    
    def test_get_command(self):
        # testing for get_command module should return self and change cur commands after run
        self.assertEqual(self.terminal.get_command('Open new tab').cur_commands, ['Open'])
        self.assertEqual(self.terminal.get_command('Task By september').cur_commands, ['By'])
        self.assertEqual(self.terminal.get_command('Create new_list Add tasks').cur_commands, ['Create', 'Add'])
        self.assertEqual(self.terminal.get_command('Rename category to new one').cur_commands, ['Rename'])
        self.assertEqual(self.terminal.get_command('Main tab').cur_commands, ['Main'])
        self.assertEqual(self.terminal.get_command('open new tab').cur_commands, [])
        self.assertEqual(self.terminal.get_command('OPEN new tab').cur_commands, [])


    def test_open_command(self):
        # if we are here -> validation is done and data in the correct form
        self.terminal.input = 'Open tasks'
        self.assertEqual(self.terminal.open_command(), 'tasks')
        self.terminal.input = 'Open new category'
        self.assertEqual(self.terminal.open_command(), 'new category')
        self.terminal.input = 'Open flowers'

    
    def test_rename_method(self):
        # if we are here -> validation is done and data in the correct form
        # simple input
        self.terminal.input = 'Rename tasks To task1'
        self.assertEqual(self.terminal.rename_command(), ['tasks', 'task1'])
        # long cat name
        self.terminal.input = 'Rename task task task To task1 task1 task1'
        self.assertEqual(self.terminal.rename_command(), ['task task task', 'task1 task1 task1'])


    def test_create_cat_add_many(self):
        # testing create cat add many method
        self.terminal.input = 'Create category Add task1, task2'
        self.assertEqual(self.terminal.create_category_add_many(),
            ['category',['task1', 'task2']])
        
        self.terminal.input  = 'Create new category Add task1, task2, task3 task4'
        self.assertEqual(self.terminal.create_category_add_many(), 
            ['new category', ['task1', 'task2', 'task3 task4']])


    def test_command_extractor(self):
        # command extractor test
        self.terminal.input = 'Create new category Add new task, task 2'
        self.assertEqual(self.terminal.command_extractor('Create', 'Add'),
            ['new category', ['new task', 'task 2']])
        
        self.terminal.input = 'Rename new category To new task'
        self.assertEqual(self.terminal.command_extractor('Rename', 'To'),
            ['new category', 'new task'])
        
        self.terminal.input = 'Open new category '
        self.assertEqual(self.terminal.command_extractor('Open'),
            ['new category'])
        
        self.terminal.input = 'Create Add task1'
        self.assertEqual(self.terminal.command_extractor('Create', 'Add'), ['task1'])

    def test_add_deadline(self):
        # deadline tests
        self.terminal.input = 'task By tomorrow'
        self.assertEqual(self.terminal.add_deadline(), [['task'], date(2021,12,2)])
        self.terminal.input = 'task By 5'
        self.assertEqual(self.terminal.add_deadline(), [['task'], date(2021,12,5)])
        self.terminal.input = 'task1 , task2 , task3 By tomorrow'
        self.assertEqual(self.terminal.add_deadline(),
             [['task1', 'task2', 'task3'], date(2021,12,2)])


    def test_validate_input(self):

        # Open category tests
        self.assertEqual(self.terminal.validate_input('Open category'), 'category')
        self.assertEqual(self.terminal.validate_input('open category'), 'open category')
        self.assertEqual(self.terminal.validate_input('Open category tail of category')
            , 'category tail of category')
        # wrong format    
        self.assertEqual(self.terminal.validate_input('Open category Open cat'), None)
        self.assertEqual(self.terminal.validate_input('Open category By'), None)

        # Rename category tests
        self.assertEqual(self.terminal.validate_input('Rename task task task To task1 task1 task1')
        , ['task task task', 'task1 task1 task1'])

        self.assertEqual(self.terminal.validate_input('Rename tasks To task1'), ['tasks', 'task1'])
               
        # wrong format
        self.assertEqual(self.terminal.validate_input('Rename tasks to task1'), None)
        self.assertEqual(self.terminal.validate_input('rename tasks To task1'), None)
        self.assertEqual(self.terminal.validate_input('rename tasks'), 'rename tasks')
        self.assertEqual(self.terminal.validate_input('rename tasks to'), 'rename tasks to')
        self.assertEqual(self.terminal.validate_input('rename to'), 'rename to')
        self.assertEqual(self.terminal.validate_input('rename tasks task1'), 'rename tasks task1')
        self.assertEqual(self.terminal.validate_input('Rename tasks To task1 To task2 To 3'), None)

        # Create add many tasks test
        self.assertEqual(self.terminal.validate_input('Create category Add task1, task2'),
            ['category',['task1', 'task2']])
        
        input  = 'Create new category Add task1, task2, task3 task4'
        self.assertEqual(self.terminal.validate_input(input), 
            ['new category', ['task1', 'task2', 'task3 task4']])

        # wrong format
        self.assertEqual(self.terminal.validate_input('Create cat Add'), None)
        self.assertEqual(self.terminal.validate_input('create cat Add task'), None)
        self.assertEqual(self.terminal.validate_input('Create Add task1'), None)
        self.assertEqual(self.terminal.validate_input('Create cat Add Add'), None)
        self.assertEqual(self.terminal.validate_input('create cat add task'),
             'create cat add task')
             
        # testing working with date manager
        self.assertEqual(self.terminal.validate_input('task By tomorrow'),
             [['task'], date(2021, 12, 2)])

        self.assertEqual(self.terminal.validate_input('task1, task2 By tomorrow'),
            [['task1', 'task2'], date(2021, 12, 2)])


if __name__ == '__main__':
    unittest.main()