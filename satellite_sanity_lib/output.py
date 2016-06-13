#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from config import C_PASS, C_WARNING, C_FAIL, C_ENDC


def color_pass(text="PASS"):
  return C_PASS + text + C_ENDC


def color_skip(text="SKIP"):
  return C_WARNING + text + C_ENDC


def color_fail(text="FAIL"):
  return C_FAIL + text + C_ENDC

output_funcs = {"PASS": color_pass,
                "SKIP": color_skip,
                "FAIL": color_fail,}
