import pprint
import ast
import re


def netlogo_representation(sequence: list):
    """

    :param sequence:
    :return:
    """

    return pprint.pformat(sequence).replace(',', ' ').replace('"', '\\').replace("'", '"')[1:-1]


def read_netlogo_representation(path):
    with open(path) as f:
        lines = f.readlines()

    lines = [line for line in lines if not line.startswith(';')]

    string = ''.join(lines).replace('][', '],[')
    string = re.sub("\s+", ",",string.strip())

    return ast.literal_eval('['+string+']')



