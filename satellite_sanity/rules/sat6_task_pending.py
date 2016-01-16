#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_6']
name = 'Ensure you do not have any Satellite 6 pending tasks'

def hostname(data):
    return data['hostname'] or None

def main(data):
    count = len(data['hammer_task_list_paused_pending']) - 1
    if count > 0:
        return {'count': count}

def text(result):
    return "You have %s tasks in 'paused' state with result 'pending'.\n" % result['count'] \
           + "Run \"hammer task list --search 'state = paused AND result = pending'\" to get the list.\n" \
           + "See https://access.redhat.com/solutions/1547743\n" \
           + "and https://access.redhat.com/solutions/1263123"
