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


if __name__ == '__main__':
    unittest.main()