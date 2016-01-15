#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity.rules import sat5_taskomatic_running

UPTIME_1 = " 21:59:49 up 10 days, 19:46,  8 users,  load average: 0.62, 10.56, 17.57".split("\n")
UPTIME_2 = " 13:53:07 up 2 days, 17:38, 16 users,  load average: 0.42, 0.35, 0.20".split("\n")
UPTIME_3 = " 08:16:42 up 17:50,  2 users,  load average: 0.16, 0.08, 0.01".split("\n")
UPTIME_4 = " 09:17:14 up 11 min,  2 users,  load average: 0.07, 0.02, 0.00".split("\n")

LINE = "root     22836  0.0  0.0  19132   500 ?        Sl   Aug25   0:44 taskomaticd"
PS_AUXCWW_YES = """postgres 21748  0.0  2.0 624688 79292 ?        Ss   Aug24   0:04 postmaster
%s
root     22838  0.7 23.3 3221620 912960 ?      Sl   Aug25  24:11 java""" % LINE
PS_AUXCWW_YES = PS_AUXCWW_YES.split("\n")
PS_AUXCWW_NO = """openvpn  22530  0.0  0.0  79116  7240 pts/1    S+   06:11   0:07 openvpn
root     22543  0.0  0.0  79116  1048 pts/1    S+   06:11   0:00 openvpn
pok      22701  1.2  5.5 3054312 901412 pts/0  Sl   Aug24  49:41 firefox""".split("\n")

class TestSat5TaskomaticRunning(unittest.TestCase):

    def test_find_taskomatic_process(self):
        self.assertEquals(None, sat5_taskomatic_running.find_taskomatic_process({'ps_auxcww': PS_AUXCWW_NO}))
        self.assertEquals({'TASKOMATIC_PROCESS_LINE': LINE}, sat5_taskomatic_running.find_taskomatic_process({'ps_auxcww': PS_AUXCWW_YES}))

    def test_get_uptime(self):
        self.assertEquals({'UPTIME_DAYS': 10}, sat5_taskomatic_running.get_uptime({'uptime': UPTIME_1}))
        self.assertEquals({'UPTIME_DAYS': 2}, sat5_taskomatic_running.get_uptime({'uptime': UPTIME_2}))
        self.assertEquals({'UPTIME_DAYS': 0}, sat5_taskomatic_running.get_uptime({'uptime': UPTIME_3}))
        self.assertEquals({'UPTIME_DAYS': 0}, sat5_taskomatic_running.get_uptime({'uptime': UPTIME_4}))

    def test_integration_match(self):
        input_data = {}
        input_data["uptime"] = UPTIME_1
        input_data["ps_auxcww"] = PS_AUXCWW_NO
        self.assertEqual(True, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_2
        input_data["ps_auxcww"] = PS_AUXCWW_NO
        self.assertEqual(True, sat5_taskomatic_running.main(input_data))

    def test_integration_no_match(self):
        input_data = {}
        input_data["uptime"] = UPTIME_3
        input_data["ps_auxcww"] = PS_AUXCWW_NO
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_4
        input_data["ps_auxcww"] = PS_AUXCWW_NO
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_1
        input_data["ps_auxcww"] = PS_AUXCWW_YES
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_2
        input_data["ps_auxcww"] = PS_AUXCWW_YES
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_3
        input_data["ps_auxcww"] = PS_AUXCWW_YES
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))

        input_data = {}
        input_data["uptime"] = UPTIME_4
        input_data["ps_auxcww"] = PS_AUXCWW_YES
        self.assertEqual(None, sat5_taskomatic_running.main(input_data))
