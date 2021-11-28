# search = '<test open_cat> flat'
# search = 'Open Hes'

# get command function looking for commands in the users input and return list of commands
# now list is useless but soon when i decide to add more complex logic it will be handy

commands = ['Open', 'Rename', 'Main']


def get_command(search):
    found_commands = []
    for command in search.split():
        if command in commands:
            found_commands.append(command)
    return found_commands
