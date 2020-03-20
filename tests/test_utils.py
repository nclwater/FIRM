import utils
import unittest

osm_file = 'tests/bwaise/bwaise.osm'

class TestUtils(unittest.TestCase):

    def test_read_netlogo_file(self):
        utils.read_netlogo_file('tests/towyn/agents.txt')

    def test_convert_terrain(self):
        utils.convert_terrain('tests/bwaise/terrain.asc', 'tests/bwaise/terrain.txt')

    def test_convert_roads(self):
        utils.convert_roads(osm_file, 'tests/bwaise/roads.txt')

    def test_convert_buildings(self):
        utils.convert_buildings(osm_file,
                        'tests/bwaise/roads.txt', 'tests/bwaise/preprocessed-buildings.txt')


if __name__ == '__main__':
    unittest.main()
