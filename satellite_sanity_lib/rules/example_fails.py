#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['demo']
name = 'Just a demo rule which keeps failing'

def main(data):
  """
  This is a fake rule which should fail (match) when hostname is shorter
  than 3 letters (i.e. in probably all cases).
  """
  if data['hostname'] is not None:
    if len(data['hostname'][0]) >= 3:
      return data['hostname'][0]

def text(result):
  """
  This function is supposed to provide more info in case of failure.
  """
  return "This text explains what is wrong, can use data returned by main()\n" \
         "'%s' and provides howto and/or links to more info" % result
