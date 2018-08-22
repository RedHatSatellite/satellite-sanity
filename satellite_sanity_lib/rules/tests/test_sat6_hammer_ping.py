#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat6_hammer_ping

GOOD = """candlepin:      
    Status:          ok
    Server Response: Duration: 46ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 15ms
pulp:           
    Status:          ok
    Server Response: Duration: 94ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 50ms
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 141ms
""".split("\n")
BAD = """candlepin:      
    Status:          ok
    Server Response: Duration: 18ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 14ms
pulp:           
    Status:          ok
    Server Response: Duration: 76ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 30ms
foreman_tasks:  
    Status:          FAIL
    Server Response:
""".split("\n")
UGLY = """candlepin:      
    Status:          ok
    Server Response: Duration: 18ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 14ms
pulp:           
    Status:          ok
    Server Response: Duration: 76ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 30ms
foreman_tasks:  
    Status:          ok
    Server Response:
""".split("\n")
MISSING = """pulp:           
    Status:          ok
    Server Response: Duration: 76ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 30ms
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 141ms
nonsense:       
    Status:          ok
    Server Response: Duration: 0ms
""".split("\n")

class TestSat6HammerPing(unittest.TestCase):
  def test_match(self):
    input_data = {'hammer_ping': BAD}
    self.assertEqual({'failed_services': set(['foreman_tasks'])}, sat6_hammer_ping.main(input_data))

  def test_match_ugly(self):
    input_data = {'hammer_ping': UGLY}
    self.assertEqual({'failed_services': set(['foreman_tasks'])}, sat6_hammer_ping.main(input_data))

  def test_match_missing(self):
    input_data = {'hammer_ping': MISSING}
    self.assertEqual({'failed_services': set(['candlepin', 'candlepin_auth', 'nonsense'])}, sat6_hammer_ping.main(input_data))

  def test_notmatch(self):
    input_data = {'hammer_ping': GOOD}
    self.assertEqual(None, sat6_hammer_ping.main(input_data))
