# search = '<test open_cat> flat'
search = 'Open Hes'

# get command function extracting <command> from user input
# as an argument function accepts string line

commands = ['Open', 'Rename', 'Main']


def get_command(search):
    found_commands = []
    for command in search.split():
        if command in commands:
            found_commands.append(command)
    return found_commands