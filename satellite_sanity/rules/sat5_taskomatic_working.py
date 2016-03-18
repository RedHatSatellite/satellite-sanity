#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5', 'Spacewalk']
name = 'Taskomatic service is not stuck'

import time
import datetime
from satellite_sanity import util

def get_current_time(data):
    return util.get_current_time(data['date'])

def get_tasko_last_log_time(data):
    date_str = data['tail_n_1_rhn_taskomatic_daemon'][-1].split("|")[2].strip()
    return datetime.datetime(*(time.strptime(date_str, '%Y/%m/%d %H:%M:%S')[0:6]))

def main(data):
    """
    Taskomatic is supposed to log something quite frequently. If it do not
    logged something in last 3 days, report it.
    """
    date_parsed = get_tasko_last_log_time(data)
    date_now = get_current_time(data)
    date_slip = datetime.timedelta(3)
    if date_parsed < date_now - date_slip:
        age = date_now - date_parsed
        return {'AGE': age.total_seconds(), 'LAST': date_parsed.strftime('%Y-%m-%d %H:%M:%S')}

def text(result):
    out = ""
    out += "Service Taskomatic does't seems to be logging its activity,\n"
    out += "maybe it is stuck? Use `service taskomatic restart` to restart it.\n"
    return out
