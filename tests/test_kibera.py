#!/usr/bin/env python
# -*- coding: utf-8 -*-


import run


vehicles = []

defences = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "rhyl1", "rhyl2", "rhyl3"]

warningtime = ["07:50:00", "07:51:00", "07:52:00", "07:53:00", "07:54:00", "07:55:00", "07:56:00", "07:57:00",
               "07:58:00", "07:59:00", "08:00:00"]

sealevel = [4, 4.2, 4.4, 4.6, 4.8, 5, 5.2, 5.4, 5.6, 5.8, 6, 6.2, 6.4, 6.6, 6.8, 7]


run.Run(in_dir='tests/kibera',
        vehicles=vehicles,
        defences=defences,
        warning_time=warningtime,
        sea_level=sealevel,
        width=297,
        height=104,
        start_time='7:45',
        end_time='8:20'
        ).run_all_setups()
