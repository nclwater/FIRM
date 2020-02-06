#!/usr/bin/env python
# -*- coding: utf-8 -*-


import run


vehicles = [
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

defences = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "rhyl1", "rhyl2", "rhyl3"]

warningtime = ["07:50:00", "07:51:00", "07:52:00", "07:53:00", "07:54:00", "07:55:00", "07:56:00", "07:57:00",
               "07:58:00", "07:59:00", "08:00:00"]

sealevel = [4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6, 6.2, 6.4, 6.6, 6.8, 7]


run.Run(in_dir='tests/towyn',
        vehicles=vehicles,
        defences=defences,
        warning_time=warningtime,
        sea_level=sealevel,
        width=249,
        height=179,
        start_time='7:45',
        end_time='8:20'
        ).run_all_setups()
