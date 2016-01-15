#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['general']
name = 'Check for ARP cache being full signs'

def main(data):
  """
  This is a fake rule which should fail (match) when hostname is shorter
  than 3 letters (i.e. in probably all cases).
  """
  for line in data['tail_n_100_var_log_messages']:
    if line.endswith('kernel: Neighbour table overflow.'):
      return {'line': line}

def text(result):
  return "Looks like your ARP table got too full recently:\n" \
         + result['line'] + \
         "See https://access.redhat.com/solutions/23454"
