#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5']
desc = 'Red Hat Satellite 5 have to be installed on this system'

def main(data):
  for line in data['installed-rpms']:
    if line.startswith('satellite-schema-'):
      return True
  return False
