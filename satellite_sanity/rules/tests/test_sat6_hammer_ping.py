#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity.rules import sat6_hammer_ping

GOOD = """candlepin:      
    Status:          ok
    Server Response: Duration: 11ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 11ms
pulp:           
    Status:          ok
    Server Response: Duration: 45ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 13ms
elasticsearch:  
    Status:          ok
    Server Response: Duration: 6ms
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 0ms
""".split("\n")
BAD = """candlepin:      
    Status:          ok
    Server Response: Duration: 11ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 10ms
pulp:           
    Status:          ok
    Server Response: Duration: 36ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 15ms
elasticsearch:  
    Status:          FAIL
    Server Response: Message: Connection refused - connect(2)
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 0ms
""".split("\n")
UGLY = """candlepin:      
    Status:          ok
    Server Response: Duration: 11ms
candlepin_auth: 
    Status:          ok
    Server Response: Duration: 10s
pulp:           
    Status:          FAIL
    Server Response: Duration: 36ms
pulp_auth:      
    Status:          ok
    Server Response: Message: Connection refused - connect(2)
elasticsearch:  
    Status:          ok
    Server Response: Duration: 15ms
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 0ms
""".split("\n")
MISSING = """pulp:           
    Status:          ok
    Server Response: Duration: 45ms
pulp_auth:      
    Status:          ok
    Server Response: Duration: 13ms
elasticsearch:  
    Status:          ok
    Server Response: Duration: 6ms
foreman_tasks:  
    Status:          ok
    Server Response: Duration: 0ms
nonsense:       
    Status:          ok
    Server Response: Duration: 0ms
""".split("\n")

class TestSat6HammerPing(unittest.TestCase):
  def test_match(self):
    input_data = {'hammer_ping': BAD}
    self.assertEqual({'failed_services': set(['elasticsearch'])}, sat6_hammer_ping.main(input_data))

  def test_match_ugly(self):
    input_data = {'hammer_ping': UGLY}
    self.assertEqual({'failed_services': set(['pulp', 'pulp_auth'])}, sat6_hammer_ping.main(input_data))

  def test_match_missing(self):
    input_data = {'hammer_ping': MISSING}
    self.assertEqual({'failed_services': set(['candlepin', 'candlepin_auth', 'nonsense'])}, sat6_hammer_ping.main(input_data))

  def test_notmatch(self):
    input_data = {'hammer_ping': GOOD}
    self.assertEqual(None, sat6_hammer_ping.main(input_data))
