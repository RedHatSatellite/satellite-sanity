#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from config import C_PASS, C_WARNING, C_FAIL, C_ENDC


def color_pass(text):
  return C_PASS + text + C_ENDC


def color_skip(text):
  return C_WARNING + text + C_ENDC


def color_fail(text):
  return C_FAIL + text + C_ENDC
