#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5', 'Satellite_6', 'Satellite_6_preinst']
name = 'Only lower-case letters allowed in hostname'

def main(data):
  if not data['hostname'] is None:
    if len(data['hostname'][0]) == 0:
      return {'error': 'Hostname output does not seem to be correct (is empty)'}
    elif not data['hostname'][0].islower():
      return {'hostname': data['hostname'][0]}

def text(result):
  out = ""
  out += "Your hostname '%s' contains uppercase letters\n" % result['hostname']
  out += "and that can cause breakage.\n"
  out += "See https://access.redhat.com/documentation/en-US/Red_Hat_Satellite/5.7/html-single/Installation_Guide/index.html#Fully_Qualified_Domain_Name_FQDN\n"
  return out
