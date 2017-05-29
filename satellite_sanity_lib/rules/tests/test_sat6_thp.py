#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat6_thp

THP_ALWAYS = ["[always] madvise never"]
THP_MADVISE = ["always [madvise] never"]
THP_NEVER = ["always madvise [never]"]

class TestTransparentHugePages(unittest.TestCase):

    def test_thp_enabled(self):
        input_data = {'thp_enabled': THP_ALWAYS}
        self.assertEquals("always", sat6_thp.thp_enabled(input_data))
        input_data = {'thp_enabled': THP_MADVISE}
        self.assertEquals("madvise", sat6_thp.thp_enabled(input_data))
        input_data = {'thp_enabled': THP_NEVER}
        self.assertEquals("never", sat6_thp.thp_enabled(input_data))

    def test_main_nomatch(self):
        input_data = {}
        input_data['thp_enabled'] = THP_NEVER
        self.assertEquals(None, sat6_thp.main(input_data))

    def test_main_match_thp(self):
        input_data = {}
        input_data['thp_enabled'] = THP_ALWAYS
        expected = {'errors': [
            "Transparent Huge Pages are set to 'always', but should be 'never'",
        ]}
        self.assertEquals(expected, sat6_thp.main(input_data))
