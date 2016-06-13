#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import hostname_matches

class TestHostnameMatches(unittest.TestCase):
  def test_nomatch(self):
    input_data = {}
    input_data['hostname'] = 'satellite.example.com'
    input_data['hn_hostname'] = 'satellite.example.com'
    input_data['sysctl_hostname'] = 'satellite.example.com'
    self.assertEqual(None, hostname_matches.main(input_data))

  def test_match(self):
    input_data = {}
    input_data['hostname'] = 'satellite'
    input_data['hn_hostname'] = 'satellite.example.com'
    input_data['sysctl_hostname'] = 'anything.example.com'
    expected = {'errors': [
        'Current hostname (satellite) and configuration in /etc/sysconfig/network (satellite.example.com) do not matches',
        'Current hostname (satellite) and configuration in /proc/sys/kernel/hostname (anything.example.com) do not matches'
    ]}
    self.assertEqual(expected, hostname_matches.main(input_data))
