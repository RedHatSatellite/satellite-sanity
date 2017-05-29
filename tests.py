#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import unittest

sys.path.append('satellite_sanity_lib/rules/tests/')

from test_example_fails import TestExampleFails
from test_sat_uppercase_hostname import TestSatUppercaseHostname
from test_sat5_correct_java import TestSat5CorrectJava
from test_sat5_taskomatic_running import TestSat5TaskomaticRunning
from test_sat5_taskomatic_working import TestSat5TaskomaticWorking
from test_sat5_rhn_charsets import TestSat5RhnCharsets
from test_sat5_diskspace_check import TestSat5DiskspaceCheck
from test_neighbour_table_overflow import TestNeighbourTableOverflow
from test_hostname_matches import TestHostnameMatches
from test_sat5_cobbler_config import TestSat5CobblerConfig
from test_sat5_hw_reqs import TestSat5HWReqs
from test_sat6_hw_reqs import TestSat6HWReqs
from test_sat6_task_pending import TestSat6TaskPending
from test_sat6_hammer_ping import TestSat6HammerPing
from test_sat6_correct_channel import TestSat6CorrectChannel
from test_sat5_frequent_osad_disconnects import TestSat5FrequentOsadDisconnects
from test_selinux import TestSELinux
from test_sat6_thp import TestTransparentHugePages

if __name__ == '__main__':
    # TODO: Also check that all rules have corresponding test module
    unittest.main()
