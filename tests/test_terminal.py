import unittest
from todoapp import terminal


class TestTerminal(unittest.TestCase):
   
   
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
        self.terminal.input = 'Open tasks'
        self.assertEqual(self.terminal.open_command(), 'tasks')
        self.terminal.input = 'Open new category'
        self.assertEqual(self.terminal.open_command(), 'new category')
        self.terminal.input = 'Open flowers'
        self.assertEqual(self.terminal.open_command(), 'flowers')
        self.terminal.input = 'open tasks'
        self.assertEqual(self.terminal.open_command(), None)
        self.terminal.input = 'command Open'
        self.assertEqual(self.terminal.open_command(), None)

    
    def test_rename_method(self):
        # simple input
        self.terminal.input = 'Rename tasks To task1'
        self.assertEqual(self.terminal.rename_command(), ['tasks', 'task1'])
        # long cat name
        self.terminal.input = 'Rename task task task To task1 task1 task1'
        self.assertEqual(self.terminal.rename_command(), ['task task task', 'task1 task1 task1'])
        # wrong format
        self.terminal.input = 'Rename tasks to task1'
        self.assertEqual(self.terminal.rename_command(), None)
        self.terminal.input = 'rename tasks To task1'
        self.assertEqual(self.terminal.rename_command(), None)
        self.terminal.input = 'rename tasks'
        self.assertEqual(self.terminal.rename_command(), None)
        self.terminal.input = 'rename tasks to'
        self.assertEqual(self.terminal.rename_command(), None)
        self.terminal.input = 'rename to'
        self.assertEqual(self.terminal.rename_command(), None)
        self.terminal.input = 'rename tasks tasks1'
        self.assertEqual(self.terminal.rename_command(), None)

if __name__ == '__main__':
    unittest.main()