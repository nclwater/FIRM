#!/usr/bin/env python
# -*- coding: utf-8 -*-


import run
import os


agents = [
    ["kids & work", "home 1", [
        ["home 1", "daily 7:46 0m", "school", 1],
        ["school", "5m 1m", "work", 0.9],
        ["school", "5m 1m", "some shop", 0.1],
        ["some shop", "2h 1h", "work", 1],
        ["work", "daily 17h 15m", "home 1", 0.75],
        ["work", "daily 17h 15m", "supermarket", 0.15],
        ["work", "daily 17h 15m", "home 2", 0.1],
        ["supermarket", "45m 10m", "home 1", 1],
        ["home 2", "daily 20h 2h", "some recreation", 0.1],
        ["some recreation", "3h 1h", "home 1", 1],

        ["evacuate", "5m 1m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "daily 4h 1h", "home 1", 1]
    ]],
    ["test2", "home", [
        ["home", "0m 0m", "school", 1],
        ["school", "0m 0m", "home", 1],

        ["evacuate", "0m 0m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "0m 0m", "home", 1],
    ]],
    ["transit eastbound", "A55 west", [
        ["A55 west", "0s 0s", "A55 east", 1],
        ["A55 east", "0s 0s", "exit", 1],
    ]],
    ["transit westbound", "A55 east", [
        ["A55 east", "0s 0s", "A55 west", 1],
        ["A55 west", "0s 0s", "exit", 1],
    ]],
    ["test", "towyn test", [
        ["towyn test", "0s 0s", "rhyl test", 1],
        ["rhyl test", "0s 0s", "towyn test", 1],

        ["evacuate", "0s 0s", "some evacuation point", 1],
        ["some evacuation point", "5m 1m", "towyn test", 1],
    ]]]

defences = ["a", "b", "c"]

warning_times = ["07:50:00", "07:51:00", "07:52:00"]

sea_levels = [4, 5, 6]

if not os.path.exists('tests/outputs'):
    os.mkdir('tests/outputs')

inputs_path = 'tests/towyn'
model_path = 'tests/outputs/towyn'

r = run.Run(model_path=model_path,
            codes_path=os.path.join(inputs_path, 'codes.txt'),
            defences_path=os.path.join(inputs_path, 'defences.txt'),
            preprocessed_buildings_path=os.path.join(inputs_path, 'preprocessed-buildings.txt'),
            roads_path=os.path.join(inputs_path, 'roads.txt'),
            terrain_path=os.path.join(inputs_path, 'terrain.txt'),
            agents=agents,
            width=249,
            height=179,
            start_time='7:45',
            end_time='8:20')

for defence in defences:
    for warning_time in warning_times:
        for sea_level in sea_levels:
            r.start(name='{}-{}-{}'.format(defence, warning_time.replace(':', '.'), sea_level), timeline=[
                    [
                        [
                            ["normal", "08:00", "15m"],
                            500,
                            ["agent", "transit eastbound"],
                            0.8,
                            ["agent", "transit westbound"],
                            0.2
                        ],
                        [
                            "0s",
                            10, # number of agents
                            ["agent", "kids & work"]
                        ],
                        [
                            "07:54",
                            ["sealevel", sea_level]
                        ],
                        [
                            "07:55",
                            ["breach", defence]
                        ],
                        [
                            warning_time,
                            ["evacuate"]
                        ]
                    ]
                ])
