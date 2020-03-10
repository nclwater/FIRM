import pprint
import ast
import re
import xml.etree.ElementTree as ET
import geopandas as gpd
from shapely.geometry import Point

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


def convert_roads(in_path, out_path, epsg=21096):
    with open(in_path) as f:
        tree = ET.fromstring(f.read())

    highways = tree.findall("way//*[@k='highway']..")
    roads = []
    for highway in highways:
        highway_id = highway.attrib['id']
        nodes = highway.findall('nd')
        lats = []
        lons = []
        ids = []
        for node in nodes:
            node_id = node.attrib['ref']
            element = tree.find("node[@id='{}']".format(node_id))
            attrib = element.attrib
            lats.append(float(attrib['lat']))
            lons.append(float(attrib['lon']))
            ids.append(node_id)

        gdf = gpd.GeoDataFrame({'id': ids,
                                'lat': lats,
                                'lon': lons,
                                'geometry': [Point(lon, lat) for lon, lat in zip(lons, lats)]
                                }, crs={'init': 'epsg:4326'}).to_crs(epsg=epsg)

        roads.append([highway_id, ids[0], ids[-1], 0, "Road Type", list(map(list, zip(gdf.geometry.x, gdf.geometry.y)))])


    with open(out_path, 'w') as f:
        f.write(netlogo_representation(roads))


