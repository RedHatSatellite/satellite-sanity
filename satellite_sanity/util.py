#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from config import logger

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
