#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_6', 'Satellite_6_preinst']
name = 'Check if Transparent Huge Pages are disabled'

from satellite_sanity_lib import util


def thp_enabled(data):
  thp_enabled = "never"
  for entry in data['thp_enabled'][0].split():
    if entry.startswith('[') and entry.endswith(']'):
      thp_enabled = entry.strip('[]')
  return thp_enabled


def main(data):
  out = []
  var_thp = thp_enabled(data)
  exp_thp = "never"
  if var_thp != exp_thp:
    out.append("Transparent Huge Pages are set to '%s', but should be '%s'" % (var_thp, exp_thp))
  if out:
    return {'errors': out}


def text(result):
  out = ""
  out += "System running Satellite 6 should not have Transparent Huge Pages enabled:\n"
  for e in result['errors']:
    out += "  %s\n" % e
  return out
