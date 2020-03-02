#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os
import shutil
import glob

from xml.etree.ElementTree import Element, SubElement

from xml.etree import ElementTree
from xml.dom import minidom
from xml.sax.saxutils import unescape


netlogo = os.environ['NETLOGO']


class Run:
    def __init__(self,
                 in_dir,
                 width,
                 height,
                 agents,
                 start_time,
                 end_time):
        self.in_dir = in_dir
        self.out_dir = os.path.join(in_dir, 'out')
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        self.nlogo_file = 'model.nlogo'
        self.setup_file = os.path.join(self.out_dir, 'setup.xml')
        self.vehicles = agents
        self.width = width
        self.height = height
        self.start_time = start_time
        self.end_time = end_time

    def write_data_file(self, filename, sequence):
        with open(self.out_dir + "/" + filename, "w") as f:
            for component in sequence:
                f.write(netlogo_representation(component))
                f.write('\n')
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
            ('Scenario', quote(str(self.in_dir))),
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
            r = os.path.join(self.out_dir, name)
            shutil.rmtree(r, True)
            os.mkdir(r)
            for f in glob.glob(self.out_dir + "/*.out"):
                shutil.copy(f, r)


def netlogo_representation(x):
    if isinstance(x, list):
        return '[' + ' '.join(map(netlogo_representation, x)) + ']'
    elif isinstance(x, str):
        r = '"'
        for c in x:
            if c == '"':
                r += '\\'
            r += c
        return r + '"'
    else:
        return repr(x)
