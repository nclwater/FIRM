import pprint
import ast
import re
import xml.etree.ElementTree as ET


def netlogo_representation(sequence: list, **kwargs):
    """

    :param sequence:
    :return:
    """

    return pprint.pformat(sequence, **kwargs).replace(',', ' ').replace('"', '\\').replace("'", '"')[1:-1]


def read_netlogo_representation(path):
    with open(path) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if not line.startswith(';')]

    string = ' '.join(lines)
    string = re.sub(r'([\d\.]+|"[\w\/\s:&]+"|\]|[^\W\s]+)', r'\1,', string)

    return ast.literal_eval('['+string+']')


def convert_terrain(in_path, out_path):

    with open(in_path) as f:
        string = netlogo_representation([line.strip().split() for line in f.readlines()])

    string = re.sub(r'"([\d\.-]+)"', r'\1', string)

    with open(out_path, 'w') as f:
        f.write(string)


def convert_roads(in_path, out_path):
    with open(in_path) as f:
        tree = ET.fromstring(f.read())

    highways = tree.findall("way//*[@k='highway']..")
    print(highways)
