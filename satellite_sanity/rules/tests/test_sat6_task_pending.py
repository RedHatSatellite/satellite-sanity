#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity.rules import sat6_task_pending

class TestSat6TaskPending(unittest.TestCase):
  def test_match(self):
    input_data = {}
    input_data['hammer_task_list_paused_pending'] = \
    """Id,Name,Owner,Started at,Ended at,State,Result,Task action,Task errors
9b4eb9a5-e21f-4fad-bd82-401ea28f0a71,,admin,2016/01/15 02:22:48,"",paused,pending,Synchronize,Abnormal termination (previous state: suspended)
c055be91-4e31-4d21-91f1-3f09cb23a300,,,2016/01/15 02:21:37,"",paused,pending,Listen on candlepin events,Abnormal termination (previous state: suspended)
990c21f3-ee59-45e8-bad2-5d4d86ff2057,,admin,2016/01/15 02:08:13,"",paused,pending,Publish,Abnormal termination (previous state: running)
863557b2-091d-4b95-8606-3d95ac90257f,,admin,2016/01/15 02:07:59,"",paused,pending,Generate Capsule Metadata and Sync,Abnormal termination (previous state: suspended)
bec05459-bb11-453c-b264-6a9dec4bba60,,,2016/01/14 18:32:01,"",paused,pending,Listen on candlepin events,Abnormal termination (previous state: suspended)""".split("\n")
    self.assertEqual({'count': 5}, sat6_task_pending.main(input_data))

  def test_notmatch(self):
    input_data = {}
    input_data['hammer_task_list_paused_pending'] = ["Id,Name,Owner,Started at,Ended at,State,Result,Task action,Task errors"]
    self.assertEqual(None, sat6_task_pending.main(input_data))
