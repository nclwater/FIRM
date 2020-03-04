import pprint
import ast


def netlogo_representation(sequence: list):
    """

    :param sequence:
    :return:
    """

    return pprint.pformat(sequence).replace(',', ' ').replace('"', '\\').replace("'", '"')[1:-1]


def read_netlogo_representation(path):
    with open(path) as f:
        string = f.read()

    new_string = ''
    in_quotes = False
    for i, char in enumerate(string):

        if char == '"':
            in_quotes = not in_quotes

        if char == ' ':
            if string[i-1] not in [' ', '\n'] and not in_quotes:
                char = ', '
        new_string += char

    return ast.literal_eval('['+new_string+']')



