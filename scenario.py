from utils import netlogo_representation
import os

class Scenario:
    def __init__(self,
                 path,
                 width,
                 height,
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
        self.width = width
        self.height = height
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

        self.create_input_files()

    def create_input_files(self):
        for sequence, filename in [

            [self.agents, 'agents.txt'],
            [self.timeline, 'timeline.txt'],
            [self.codes, 'codes.txt'],
            [self.defences, 'defences.txt'],
            [self.buildings, 'preprocessed-buildings.txt'],
            [self.roads, 'roads.txt'],
            [self.terrain, 'terrain.txt'],
            [self.streams, 'streams.txt']
        ]:
            if sequence is not None:
                self.write_data_file(filename, sequence)

    def write_data_file(self, filename, sequence):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(self.path + "/" + filename, "w") as f:
            f.write(netlogo_representation(sequence))
            f.close()
