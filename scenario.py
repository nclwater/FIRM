class Scenario:
    def __init__(self, path, agents, timeline, codes, defences, buildings, roads, terrain, streams=None):
        self.path = path
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

    def create_setup_file(self):
        pass
