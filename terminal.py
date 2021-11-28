# search = '<test open_cat> flat'

# get command function extracting <command> from user input
# as an argument function accepts string line


def get_command(search):
    # splitting by the first command char '<'
    split_by_command = search.split('<')
    # if length of the split is equal to 1 it means we do not have received a command
    # or it was written in the wrong way
    # the function returns empty sting
    if len(split_by_command) == 1:
        return ''
    else:
        # getting command value
        command_value = split_by_command[1]
        # split '>' to get rid of '>'
        split_by_command_last = command_value.split('>')
        # getting cleaned command value and returning it
        command_value = split_by_command_last[0]
        return command_value
