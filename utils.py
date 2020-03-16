import pprint
import ast
import re
import xml.etree.ElementTree as ET
import numpy as np
# import geopandas as gpd
# from shapely.geometry import Point
import ogr, osr
from scipy.spatial.distance import cdist
from scipy.spatial import cKDTree

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


def convert_roads(in_path, out_path, **kwargs):
    with open(in_path) as f:
        tree = ET.fromstring(f.read())

    highways = tree.findall("way//*[@k='highway']..")
    roads = []
    for highway in highways:
        highway_id = highway.attrib['id']
        nodes = highway.findall('nd')
        highway_type = highway.find("*[@k='highway']").attrib['v']
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

        x, y = reproject(lats, lons, **kwargs)

        distance = cdist(np.transpose([x[:-1], y[:-1]]), np.transpose([x[1:], y[1:]])).sum().round(0).astype(int)

        roads.append([highway_id, ids[0], ids[-1], distance, highway_type, list(map(list, zip(x, y)))])


    with open(out_path, 'w') as f:
        f.write(netlogo_representation(roads))


def convert_buildings(in_path, roads_path, out_path, **kwargs):
    with open(in_path) as f:
        tree = ET.fromstring(f.read())

    roads = read_netlogo_representation(roads_path)
    x = []
    y = []
    node_ids = []

    for road in roads:
        _, origin, destination, _, _, coords = road
        origin_x, origin_y = coords[0]
        destination_x, destination_y = coords[-1]
        node_ids.append(origin)
        x.append(origin_x)
        y.append(origin_y)

        node_ids.append(destination)
        x.append(destination_x)
        y.append(destination_y)

    nodes_kd_tree = cKDTree(np.transpose([x, y]))

    buildings = tree.findall("way//*[@k='building']..")
    roads = []
    for building in buildings:
        # highway_id = building.attrib['id']
        nodes = building.findall('nd')
        # building_type = building.find("*[@k='building']").attrib['v']
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

        x, y = np.mean(np.transpose(reproject(lats, lons, **kwargs)), axis=0)
        _, index = nodes_kd_tree.query([[x, y]])

        roads.append([x, y, 0, node_ids[index[0]]])


    with open(out_path, 'w') as f:
        f.write(netlogo_representation(roads))



def reproject(lats, lons, epsg=21096):
    src = osr.SpatialReference()
    src.ImportFromEPSG(4326)
    dest = osr.SpatialReference()
    dest.ImportFromEPSG(epsg)
    transform = osr.CoordinateTransformation(src, dest)

    x = []
    y = []

    for lat, lon in zip(lats, lons):
        point = ogr.CreateGeometryFromWkt("POINT ({} {})".format(lat, lon))
        point.Transform(transform)
        x.append(point.GetX())
        y.append(point.GetY())

    return x, y
