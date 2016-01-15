#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest


from satellite_sanity.rules import example_fails

class TestExampleFails(unittest.TestCase):
  def test_example_failing(self):
    self.assertEqual('example.com', example_fails.main({'hostname': ['example.com']}))
    self.assertEqual(None, example_fails.main({'hostname': ['x']}))
    self.assertEqual(None, example_fails.main({'hostname': None}))
