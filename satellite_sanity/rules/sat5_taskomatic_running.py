#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5', 'Spacewalk']
name = 'Taskomatic service is running'

from satellite_sanity.util import get_days_uptime

def find_taskomatic_process(data):
    """
    Check the ps output to see if taskomatic is running
    """
    for line in data['ps_auxcww']:
        if line.endswith(' taskomaticd'):
            return {'TASKOMATIC_PROCESS_LINE': line}


def get_uptime(data):
    """
    Return the number of days the machine has been up
    """
    return {'UPTIME_DAYS': int(get_days_uptime(data['uptime'][0]))}


def main(data):
    if data['ps_auxcww'] is not None or data['uptime'] is not None:
        # We do not want to hit case when system just booted, Satellite
        # is still starting (taskomatic not yet running)
        if get_uptime(data)['UPTIME_DAYS'] > 0:
            if not find_taskomatic_process(data):
                return True

def text(result):
    out = ""
    out += "Service Taskomatic does't seems to be running.\n"
    out += "Use `service taskomatic restart` to restart it.\n"
    out += "For more info check https://access.redhat.com/solutions/232243"
    return out
