#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest


from satellite_sanity_lib.rules import sat_uppercase_hostname

class TestSatUppercaseHostname(unittest.TestCase):
  def test_match(self):
    self.assertEqual({'hostname': 'SATELLITE.EXAMPLE.COM'}, sat_uppercase_hostname.main({'hostname': ['SATELLITE.EXAMPLE.COM']}))
    self.assertEqual({'hostname': 'SATELLITE.example.com'}, sat_uppercase_hostname.main({'hostname': ['SATELLITE.example.com']}))
    self.assertEqual({'hostname': 'Satellite.example.com'}, sat_uppercase_hostname.main({'hostname': ['Satellite.example.com']}))

  def test_no_match(self):
    self.assertEqual(None, sat_uppercase_hostname.main({'hostname': None}))
    self.assertEqual(None, sat_uppercase_hostname.main({'hostname': ['dhcp131-38.something.example.com']}))

  def test_error(self):
    self.assertEqual({'error': 'Hostname output does not seem to be correct (is empty)'}, sat_uppercase_hostname.main({'hostname': ['']}))
