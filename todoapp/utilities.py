class ExtractCommand:


    def extract_single_command_value(input):
        # Comand .......
        value = input.split()[1:]
        return ' '.join(value)


    def extract_middle_value(input, seperator):
        # Add ..middlevalue.. By...
        # seperator value should be defined to use this method
        input_split = input.split()
        index_of_seperator = input_split.index(seperator)
        value = input_split[1:index_of_seperator]
        value = ' '.join(value)
        return value


    def extract_after_value(input, seperator):
        # Comand .... Command 2 ....after value....
        # Comand some values Seperator after seperator values
        input_split = input.split()
        index_of_seperator = input_split.index(seperator)
        value = input_split[index_of_seperator+1:]
        value = ' '.join(value)
        return value

