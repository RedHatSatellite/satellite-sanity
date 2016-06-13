#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import datetime
import time

from satellite_sanity_lib.rules import sat5_taskomatic_working

# Later in the tests we can not compare for equality, becase when we specify
# TIME_NOW here, it have nanoseconds as well, but time format used in
# rhn_taskomatic_daemon.log do not have that, so datetime object created by
# parsing that have nanoseconds set to 0 every time
LINE = "INFO   | jvm 1    | %s | %s,099 [DefaultQuartzScheduler_Worker-7] INFO  com.redhat.rhn.taskomatic.task.SessionCleanup - 1 stale session(s) deleted"

TIME_OLD = '2015/12/15 08:05:14'
TIME_RECENT = '2015/12/20 07:05:41'
TIME_FUTURE = '2015/12/20 10:06:17'
TIME_OLD2 = '2015-12-15 08:05:14'
TIME_RECENT2 = '2015-12-20 07:05:41'
TIME_FUTURE2 = '2015-12-20 10:06:17'

DATE = 'Sun Dec 20 08:01:27 CET 2015'
DATE_PARSED = datetime.datetime(2015, 12, 20, 8, 01, 27)

FORMAT_TASKO = '%Y/%m/%d %H:%M:%S'

class TestSat5TaskomaticWorking(unittest.TestCase):

    def test_get_current_time(self):
        input_data = {'date': [DATE]}
        self.assertEqual(DATE_PARSED, sat5_taskomatic_working.get_current_time(input_data))

    def test_get_tasko_last_log_time(self):
        input_data = {'tail_n_1_rhn_taskomatic_daemon': [LINE % (TIME_OLD, TIME_OLD2)]}
        parsed = datetime.datetime.strptime(TIME_OLD, FORMAT_TASKO)
        self.assertEqual(parsed, sat5_taskomatic_working.get_tasko_last_log_time(input_data))
        input_data = {'tail_n_1_rhn_taskomatic_daemon': [LINE % (TIME_RECENT, TIME_RECENT2)]}
        parsed = datetime.datetime.strptime(TIME_RECENT, FORMAT_TASKO)
        self.assertEqual(parsed, sat5_taskomatic_working.get_tasko_last_log_time(input_data))
        input_data = {'tail_n_1_rhn_taskomatic_daemon': [LINE % (TIME_FUTURE, TIME_FUTURE2)]}
        parsed = datetime.datetime.strptime(TIME_FUTURE, FORMAT_TASKO)
        self.assertEqual(parsed, sat5_taskomatic_working.get_tasko_last_log_time(input_data))

    def test_match(self):
        input_data = {}
        input_data['date'] = [DATE]
        input_data['tail_n_1_rhn_taskomatic_daemon'] = [LINE % (TIME_OLD, TIME_OLD2)]
        expected = {'AGE': 431773.0, 'LAST': '2015-12-15 08:05:14'}
        self.assertEqual(expected, sat5_taskomatic_working.main(input_data))

    def test_no_match(self):
        input_data = {}
        input_data['date'] = [DATE]
        input_data['tail_n_1_rhn_taskomatic_daemon'] = [LINE % (TIME_RECENT, TIME_RECENT2)]
        self.assertEqual(None, sat5_taskomatic_working.main(input_data))
        input_data = {}
        input_data['date'] = [DATE]
        input_data['tail_n_1_rhn_taskomatic_daemon'] = [LINE % (TIME_FUTURE, TIME_FUTURE2)]
        self.assertEqual(None, sat5_taskomatic_working.main(input_data))
