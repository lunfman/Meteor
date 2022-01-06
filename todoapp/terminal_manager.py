from .terminal import Terminal
from . import commands
from flask import request
from .some_func import return_back
from .db_actions import DbActions

def terminal_manager(input):
    terminal = Terminal(input)
    terminal.add_command(commands.MainCommand)
    terminal.add_command(commands.OpenCommand)
    terminal.add_command(commands.RenameCommand)
    terminal.add_command(commands.CreateCommand)
    terminal.add_command(commands.ByCommand)
    terminal.add_command(commands.ShowCommand)
    terminal.add_command(commands.AddCommand)
    terminal.add_command(commands.HelpCommand)
    terminal.add_command(commands.RevealCommand)
    terminal.add_command(commands.HideCommand)
    terminal.add_command(commands.DeleteCommand)
    terminal.add_command(commands.MigrateCommand)

    run = terminal.execute_command()
    if run == 'command not found':
        category_name = request.args.get('category')
        # commands.AddTask(input, category_name)
        DbActions.create_task(input, category_name)
        return return_back()
    elif run == 'not valid input':
        return return_back()
    return run