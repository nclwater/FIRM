from xml.etree.ElementTree import Element, SubElement

from xml.etree import ElementTree
from xml.dom import minidom
from xml.sax.saxutils import unescape


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

    def create_setup_file(self, seed=1):

        experiments = Element('experiments')

        experiment = SubElement(experiments, 'experiment',
                                dict(name='toytown', repetitions="1", runMetricsEveryStep='false'))

        setup = SubElement(experiment, 'setup')
        setup.text = 'setup pathshow-setup'

        go = SubElement(experiment, 'go')
        go.text = 'model-step'

        final = SubElement(experiment, 'final')
        final.text = 'write-final-report'

        exit_condition = SubElement(experiment, 'exitCondition')
        exit_condition.text = 'ticks &gt; end-time'

        metric = SubElement(experiment, 'metric')
        metric.text = '(list end-time agents-drowned agents-diverted agents-isolated)'

        def quote(string):
            return "&quot;{}&quot;".format(string)

        for variable, value in [
            ('start-time', quote(self.start_time)),
            ('Scenario', quote(str(self.model_path))),
            ('heuristic-factor', '1.25'),
            ('log-interval', quote('2m')),
            ('end-time-str', quote(self.end_time)),
            ('random-seed', str(seed)),
            ('world-width', str(self.width)),
            ('world-height', str(self.height))

        ]:
            element = SubElement(experiment, 'enumeratedValueSet', {'variable': variable})
            SubElement(element, 'value', {'value': value})
        header = r'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE experiments SYSTEM "behaviorspace.dtd">'
        dom = minidom.parseString(header + ElementTree.tostring(experiments).decode('utf-8'))
        with open(self.setup_file, 'w') as f:
            f.write(unescape(dom.toprettyxml()))
