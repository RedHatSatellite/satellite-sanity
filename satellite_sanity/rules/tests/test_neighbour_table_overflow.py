#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

CLEAN = [
  'Dec  4 00:38:13 elisha dhclient[1435]: DHCPREQUEST on eth0 to 10.38.5.26 port 67 (xid=0x68fe265e)',
  'Dec  4 00:38:13 elisha dhclient[1435]: DHCPACK from 10.38.5.26 (xid=0x68fe265e)',
  'Dec  4 00:38:15 elisha dhclient[1435]: bound to 10.34.130.126 -- renewal in 40323 seconds.',
  'Dec  4 04:28:39 elisha rhsmd: This system is registered to RHN Classic.',
  'Dec  4 06:13:49 elisha yum[6132]: Installed: 2:nmap-5.51-4.el6.x86_64'
]
OVER = [
  'Dec  4 06:21:22 elisha kernel: Neighbour table overflow.',
  'Dec  4 06:21:37 elisha kernel: Neighbour table overflow.'
]

from satellite_sanity.rules import neighbour_table_overflow

class TestNeighbourTableOverflow(unittest.TestCase):
  def test_main(self):
    input_data = {'tail_n_100_var_log_messages': CLEAN}
    self.assertEqual(None, neighbour_table_overflow.main(input_data))
    input_data = {'tail_n_100_var_log_messages': CLEAN+OVER}
    expected = {'line': 'Dec  4 06:21:22 elisha kernel: Neighbour table overflow.'}
    self.assertEqual(expected, neighbour_table_overflow.main(input_data))
