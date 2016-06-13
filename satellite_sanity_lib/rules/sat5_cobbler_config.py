#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

tags = ['Satellite_5', 'Spacewalk']
name = 'Basic Cobbler settings are correct'

def etc_cobbler_settings(data):
  """
  Verify settings in /etc/cobbler/settings:
    redhat_management_type: "site"
    redhat_management_server: "satellite.example.com"
    server: satellite.example.com
  Teoretically we can have one option specified multiple times, so we want
  to evaluate only last one.
  """
  out = []
  opts_found = 0
  hostname = data['hostname'][0]
  etc_cobbler_settings_redhat_management_type = ''
  etc_cobbler_settings_redhat_management_server = ''
  etc_cobbler_settings_server = ''

  for line in data['etc_cobbler_settings']:
    if re.match('^\s*redhat_management_type\s*:', line):
      opts_found += 1
      val = line.split(':')[1].strip()
      if re.search(r'[\'"]?\bsite\b[\'"]?', val):
        etc_cobbler_settings_redhat_management_type = ''
      else:
        etc_cobbler_settings_redhat_management_type = 'In /etc/cobbler/settings there should be \'redhat_management_type: "site"\''

    if re.match('^\s*redhat_management_server\s*:', line):
      opts_found += 1
      val = line.split(':')[1].strip()
      if re.search(r'[\'"]?\b%s\b[\'"]?' % hostname, val):
        etc_cobbler_settings_redhat_management_server = ''
      else:
        etc_cobbler_settings_redhat_management_server = 'In /etc/cobbler/settings there should be \'redhat_management_server: %s\'' % hostname

    if re.match('^\s*server\s*:', line):
      opts_found += 1
      val = line.split(':')[1].strip()
      if re.search(r'[\'"]?\b%s\b[\'"]?' % hostname, val):
        etc_cobbler_settings_server = ''
      else:
        etc_cobbler_settings_server = 'In /etc/cobbler/settings there should be \'server: %s\'' % hostname

  if opts_found != 3:
    out.append("Not all of redhat_management_type, redhat_management_server and server options found in /etc/cobbler/settings")
  for o in (etc_cobbler_settings_redhat_management_type, etc_cobbler_settings_redhat_management_server, etc_cobbler_settings_server):
    if o != '':
      out.append(o)
  return out

def etc_cobbler_modules_conf(data):
  """
  Verify settings in /etc/cobbler/modules.conf:
    [authentication]
    module = authn_spacewalk
  """
  out = []
  opts_found = 0
  etc_cobbler_modules_conf_authentication_module = ''
  section_auth = False

  for line in data['etc_cobbler_modules_conf']:
    if re.match('^\s*\[.*\]\s*$', line):
      section_auth = False
      if re.match('^\s*\[authentication\]\s*$', line):
        section_auth = True
      continue
    if section_auth and re.match('^\s*module\s*=', line):
      opts_found += 1
      val = line.split('=')[1].strip()
      if re.search(r'[\'"]?\bauthn_spacewalk\b[\'"]?', val):
        etc_cobbler_modules_conf_authentication_module = ''
      else:
        etc_cobbler_modules_conf_authentication_module = 'In /etc/cobbler/modules.conf there should be \'module = authn_spacewalk\''

  if opts_found != 1:
    out.append("Option module in section authentication not found in /etc/cobbler/modules.conf")
  for o in (etc_cobbler_modules_conf_authentication_module,):
    if o != '':
      out.append(o)
  return out

def main(data):
  """
  For hostname check noticed in the KB article we have different rule, we are
  missing chack for hostname/ip in /etc/hosts though.
  """
  out = []
  out += etc_cobbler_settings(data)
  out += etc_cobbler_modules_conf(data)
  if out:
    return {'errors': out}

def text(result):
  out = ""
  out += "Certain config options in Cobbler configuratin should be set as expected:\n"
  for e in result['errors']:
    out += "  %s\n" % e
  out += "See https://access.redhat.com/solutions/27936"
  return out
