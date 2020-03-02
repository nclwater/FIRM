#!/usr/bin/env python
# -*- coding: utf-8 -*-


import run


agents = [
    ["kids", "home 1", [
        ["home 1", "daily 6:05 15m", "school",  0.9],
        ["home 1", "daily 6:05 3h", "some other", 0.1],
        ["school", "daily 15:00 30m", "home 1", 0.5],
        ["school", "daily 15:00 30m", "some other", 0.5],
        ["some other", "3h 1h", "home 1", 1],
        ["evacuate", "5m 1m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "daily 4h 1h", "home 1", 1]
     ]],
    ["teenagers", "home 1", [
        ["home 1", "daily 6:05 15m", "school",  0.58],
        ["home 1", "daily 6:05 1h", "work",  0.2],
        ["home 1", "daily 6:05 3h", "some other", 0.22],
        ["work", "daily 8:00 1h", "some other", 0.3],
        ["work", "daily 8:00 3h", "home 1", 0.2],
        ["school", "daily 15:00 30m", "home 1", 0.5],
        ["school", "daily 15:00 30m", "some other", 0.5],
        ["work", "daily 16:00 10m", "home 1", 1],
        ["some other", "3h 1h", "home 1", 1],
        ["evacuate", "5m 1m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "daily 4h 1h", "home 1", 1]
    ]],
    ["Men", "home 1", [
        ["home 1", "daily 6:05 0m", "some work",  0.6],
        ["home 1", "daily 6:05 1h", "some other", 0.4],
        ["some other", "daily 16:00 5m", "some other", 1],
        ["some work", "daily 16:00 5m", "home 1", 0.6],
        ["some work", "daily 16:00 5m", "some shop", 0.2],
        ["some work", "daily 16:00 5m", "some other", 0.2],
        ["some other", "3h 1h", "home 1", 1],
        ["some shop", "3h 1h", "home 1", 1],
        ["evacuate", "5m 1m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "daily 4h 1h", "home 1", 1],
    ]],
    ["Women", "home 1", [
        ["home 1", "daily 6:05 0m", "school",  0.5],
        ["home 1", "daily 6:05 0m", "some shop", 0.5],
        ["school", "1h 20m", "home 2", 0.9],
        ["school", "30m 1m", "some shop", 0.1],
        ["home 2", "daily 16:00 0m", "school", 1],
        ["some shop", "daily 16:00 5m", "home 1", 0.6],
        ["some shop", "daily 16:00 5m", "some other", 0.4],
        ["school", "30m 0m", "home 1", 1],
        ["some other", "3h 1h", "home 1", 1],
        ["evacuate", "5m 1m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "daily 4h 1h", "home 1", 1]
    ]],
    ["transit eastbound", "Road1", [
        ["Road1", "0s 0s", "Road2", 1],
        ["Road2", "0s 0s", "exit", 1]
    ]],
    ["transit westbound", "Road2", [
        ["Road2", "0s 0s", "Road3", 1],
        ["Road3", "0s 0s", "exit", 1]
    ]],
    ["transit northbound", "Road3", [
        ["Road3", "0s 0s", "Road1", 1],
        ["Road1", "0s 0s", "exit", 1]
    ]],
    ["test2", "home", [
        ["home", "0m 0m", "school", 1],
        ["school", "0m 0m", "home", 1],
        ["evacuate", "0m 0m", "some evacuation point", 0.9],
        ["evacuate", "0s 0s", "resume", 0.1],
        ["some evacuation point", "0m 0m", "home", 1]
    ]]
]

defences = ["a", "b", "c"]

warning_times = ["07:50:00", "07:55:00", "08:00:00"]

sea_levels = [4, 5, 6]


r = run.Run(in_dir='tests/kibera',
            agents=agents,
            width=297,
            height=104,
            start_time='7:45',
            end_time='8:20')


for defence in defences:
    for warning_time in warning_times:
        for sea_level in sea_levels:
            r.start(name='{}-{}-{}'.format(defence, warning_time.replace(':', '.'), sea_level),
                    timeline=
                    [
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
                            ["agent", "kids"]
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
                ]
                    )
