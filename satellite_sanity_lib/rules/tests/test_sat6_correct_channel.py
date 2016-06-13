#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat6_correct_channel

EMPTY = ["This system is not yet registered. Try 'subscription-manager register --help' for more information."]
YREL = ["Release: 6.4"]
DEFAULT = ["Release not set"]
CORRECT = ["Release: 6Server"]

class TestSat6CorrectChannel(unittest.TestCase):
  def test_empty(self):
    input_data = {'rhsm_release_show': EMPTY}
    self.assertEqual({'msg': 'You are not registered using subscription-manager'}, sat6_correct_channel.main(input_data))

  def test_y_release(self):
    input_data = {'rhsm_release_show': YREL}
    self.assertEqual({'msg': 'Your release is set to 6.4, but should be one of 6Server, 7Server'}, sat6_correct_channel.main(input_data))

  def test_default(self):
    input_data = {'rhsm_release_show': DEFAULT}
    self.assertEqual(None, sat6_correct_channel.main(input_data))

  def test_correct(self):
    input_data = {'rhsm_release_show': CORRECT}
    self.assertEqual(None, sat6_correct_channel.main(input_data))
