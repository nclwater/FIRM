#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil
import pprint
from shutil import copyfile

from xml.etree.ElementTree import Element, SubElement

from xml.etree import ElementTree
from xml.dom import minidom
from xml.sax.saxutils import unescape


netlogo = os.environ['NETLOGO']


class Run:
    def __init__(self,
                 model_path,
                 codes_path,
                 defences_path,
                 preprocessed_buildings_path,
                 roads_path,
                 terrain_path,
                 width,
                 height,
                 agents,
                 start_time,
                 end_time,
                 streams_path=None):
        """"

        Agents structure:

        [
            [
                agent_type,
                agent_location,
                [
                    origin,
                    time,
                    destination,
                    probability
                ]
            ]
        ]

        """
        self.model_path = model_path
        if not os.path.exists(model_path):
            os.mkdir(model_path)

        for src, dest in [
            [codes_path, 'codes.txt'],
            [defences_path, 'defences.txt'],
            [preprocessed_buildings_path, 'preprocessed-buildings.txt'],
            [roads_path, 'roads.txt'],
            [terrain_path, 'terrain.txt'],
            [streams_path, 'streams.txt']
        ]:
            if src is not None:
                copyfile(src, self.path(dest))

        self.nlogo_file = 'model.nlogo'
        self.setup_file = self.path('setup.xml')
        self.vehicles = agents
        self.width = width
        self.height = height
        self.start_time = start_time
        self.end_time = end_time

    def write_data_file(self, filename, sequence):
        with open(self.model_path + "/" + filename, "w") as f:
            f.write(netlogo_representation(sequence))
            f.close()

    def write_setup_file(self, seed):

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

    def run(self):
        args = ['java',
                '-Xmx1024M',
                '-cp',
                netlogo,
                'org.nlogo.headless.HeadlessWorkspace',
                '--table',
                'table-output.csv',
                '--model',
                self.nlogo_file,
                '--setup-file',
                self.setup_file,
                '--experiment',
                'toytown']
        p = subprocess.Popen(args)
        p.wait()
        print("done with %s" % str(p.returncode))

    def start(self, name, timeline, seed=None):
        if seed is None:
            seed = [0]

        self.write_data_file('agents.txt', self.vehicles)
        for sc in seed:
            self.write_data_file('timeline.txt', timeline)
            self.write_setup_file(sc)
            self.run()
            results_path = self.path(name)
            shutil.rmtree(results_path, True)
            os.mkdir(results_path)
            for f in os.listdir(self.model_path):
                if f.endswith('.out'):
                    shutil.copy(self.path(f), results_path)

    def path(self, path):
        return os.path.join(self.model_path, path)


def netlogo_representation(sequence: list):
    """

    :param sequence:
    :return:
    """

    return pprint.pformat(sequence).replace(',', ' ').replace('"', '\\').replace("'", '"')[1:-1]
