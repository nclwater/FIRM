import utils

utils.read_netlogo_representation('tests/towyn/agents.txt')

utils.convert_terrain('tests/bwaise/terrain.asc', 'tests/bwaise/terrain.txt')

utils.convert_roads('tests/bwaise/bwaise.osm', 'tests/bwaise/roads.txt')

utils.convert_buildings('tests/bwaise/bwaise.osm',
                        'tests/bwaise/roads.txt', 'tests/bwaise/preprocessed-buildings.txt')
