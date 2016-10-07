#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['general']
name = 'SELinux should be enabled and enforcing'

def main(data):
  if not data['selinux'] is None:
    # Determine where link currently points to
    status = None
    mode  = None
    for line in data['selinux']:
      if line.startswith('SELinux status:'):
        status = line.split()[-1]
      elif line.startswith('Current mode:'):
        mode = line.split()[-1]

      if status and mode:
        break;

    # Evaluate
    if not((status == "enabled") and (mode == "enforcing")):
      return {'status' : status, 'mode' : mode}

def text(result):
  out = ""
  out += "Red Hat suggests that SELinux be enabled and enforcing.\n"
  out += "Current status is '%s'\n" % result['status']
  out += "Current mode is '%s'\n" % result['mode']
  return out
