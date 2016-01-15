#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['general']
name = 'Check that hostname is configured properly'

def hn_hostname(data):
  return data['hn_hostname'] or None

def sysctl_hostname(data):
  return data['sysctl_hostname'] or None

def hostname(data):
  return data['hostname'] or None

def main(data):
  out = []
  var_hn_hostname = hn_hostname(data)
  var_sysctl_hostname = sysctl_hostname(data)
  var_hostname = hostname(data)
  if var_hostname is not None \
     and var_hn_hostname is not None \
     and var_hostname != var_hn_hostname:
    out.append('Current hostname (%s) and configuration in /etc/sysconfig/network (%s) do not matches' % (var_hostname, var_hn_hostname))
  if var_hostname is not None \
     and var_sysctl_hostname is not None \
     and var_hostname != var_sysctl_hostname:
    out.append('Current hostname (%s) and configuration in /proc/sys/kernel/hostname (%s) do not matches' % (var_hostname, var_sysctl_hostname))
  if out:
      return {'errors': out}

def text(result):
  return "Hostname is not configured properly:\n" \
         + "\n".join(result['errors']) + \
         "This is required for spacewalk-hostname-rename"
