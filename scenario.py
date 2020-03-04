import pprint

class Scenario:
    def __init__(self,
                 path,
                 start_time,
                 end_time,
                 agents,
                 timeline,
                 codes,
                 defences,
                 buildings,
                 roads,
                 terrain,
                 streams=None):
        self.path = path
        self.start_time = start_time
        self.end_time = end_time
        self.agents = agents
        self.timeline = timeline
        self.codes = codes
        self.defences = defences
        self.buildings = buildings
        self.roads = roads
        self.terrain = terrain
        self.streams = streams

    def create_input_files(self):
        pass

    def write_data_file(self, filename, sequence):
        with open(self.path + "/" + filename, "w") as f:
            f.write(netlogo_representation(sequence))
            f.close()

def netlogo_representation(sequence: list):
    """

    :param sequence:
    :return:
    """

    return pprint.pformat(sequence).replace(',', ' ').replace('"', '\\').replace("'", '"')[1:-1]
