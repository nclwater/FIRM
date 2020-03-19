import utils
import unittest


class TestUtils(unittest.TestCase):

    def test_read_netlogo_file(self):
        utils.read_netlogo_file('tests/towyn/agents.txt')

    def test_convert_terrain(self):
        utils.convert_terrain('tests/bwaise/terrain.asc', 'tests/bwaise/terrain.txt')

    def test_convert_roads(self):
        utils.convert_roads('tests/bwaise/bwaise.osm', 'tests/bwaise/roads.txt')

    def test_convert_buildings(self):
        utils.convert_buildings('tests/bwaise/bwaise.osm',
                        'tests/bwaise/roads.txt', 'tests/bwaise/preprocessed-buildings.txt')


if __name__ == '__main__':
    unittest.main()
