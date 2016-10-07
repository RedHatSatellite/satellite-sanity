#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import selinux


SELINUX_CORRECT = """SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          permissive
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      30""".split("\n")

SELINUX_BAD_STATUS = """SELinux status:                 disabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          permissive
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      30""".split("\n")

SELINUX_BAD_MODE = """SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   permissive
Mode from config file:          permissive
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      30""".split("\n")


class TestSELinux(unittest.TestCase):

    def test_good(self):
        input_data = {}
        input_data['selinux'] = SELINUX_CORRECT
        self.assertEquals(None, selinux.main(input_data))

    def test_bad_status(self):
        input_data = {}
        input_data['selinux'] = SELINUX_BAD_STATUS
        expected = {'status' : 'disabled', 'mode' : 'enforcing'}
        self.assertEquals(expected, selinux.main(input_data))

    def test_bad_mode(self):
        input_data = {}
        input_data['selinux'] = SELINUX_BAD_MODE
        expected = {'status' : 'enabled', 'mode' : 'permissive'}
        self.assertEquals(expected, selinux.main(input_data))
