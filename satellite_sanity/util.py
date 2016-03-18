#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import dateutil.parser
from config import logger

def get_current_time(date):
  assert len(date) == 1
  return dateutil.parser.parse(date[0], ignoretz=True)

def get_days_uptime(uptime):
  """Return number of days from uptime"""
  # FIXME: what happens when system have uptime in years?
  # Maybe http://bytes.com/topic/python/answers/36189-uptime-unix#td_post_135199
  ###logger.debug("Going to parse %s" % uptime)
  uptime_split = uptime.strip().split(' ')
  if uptime_split[3] == 'days,':
    return int(uptime_split[2])
  elif uptime_split[3] == 'day,':
    return int(uptime_split[2])
  else:
    return 0


def os_arch(uname_a):
  """
  Return architecture we are running on.
  """
  assert len(uname_a) == 1
  return uname_a[0].split()[-2]


def cpu_speed(proc_cpuinfo, uname_a):
  """
  Return processor speed on x86_64.   FIXME: what about processor scaling?
  Returns None on s390x.
  """
  if os_arch(uname_a) == 'x86_64':
    for line in proc_cpuinfo:
      if line.startswith('cpu MHz'):
        val = line.split(':')[1].strip()
        return float(val)


def cpu_cache(proc_cpuinfo, uname_a):
  """
  Return CPU cache size.
  Returns None on s390x.
  """
  if os_arch(uname_a) == 'x86_64':
    for line in proc_cpuinfo:
      if line.startswith('cache size'):
        val = line.split(':')[1].strip().replace(' KB', '')
        return float(val)


def cpu_cores(proc_cpuinfo):
  """
  Return number of CPU cores.
  """
  count = 0
  for line in proc_cpuinfo:
    if line.startswith('processor'):
      count += 1
  return count


def __val_from_proc_meminfo(proc_meminfo, label):
  """
  Return value in kB for given label (like 'MemTotal' or 'SwapTotal') from
  structure of /proc/meminfo
  """
  for line in proc_meminfo:
    if line.startswith('%s:' % label):
      val = line.split(':')[1].strip().replace(' kB', '')
      return float(val)


def ram_size(proc_meminfo):
  """
  Return RAM size in kB.
  """
  return __val_from_proc_meminfo(proc_meminfo, 'MemTotal')


def swap_size(proc_meminfo):
  """
  Return swap size in kB.
  """
  return __val_from_proc_meminfo(proc_meminfo, 'SwapTotal')


def satellite5_version(installed_rpms):
    for line in installed_rpms:
        if line.startswith('satellite-schema-'):
            return line.replace('satellite-schema-', '')


def satellite5_is_emb_pg(rhn_conf):
    """
    Return true if we are running on Satellite with embedded PostgreSQL
    """
    for line in rhn_conf:
        if line.startswith('db_backend'):
            backend = line.split('=')[1].strip()
            if backend != 'postgresql':
                return False
        if line.startswith('db_host'):
            backend = line.split('=')[1].strip()
            if backend != '':
                return False
    return True
