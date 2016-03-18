#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5', 'Spacewalk']
name = 'Make sure osad on client is not disconnecting frequently'

import datetime
import dateutil.parser
import re
from satellite_sanity import util

INTERVAL = 72   # check only log messages not older than 72 hours


def get_current_time(data):
    return util.get_current_time(data['date'])


def indicator_syslog(data, date):
    """Return list of relevant lines from /var/log/messages newer than provided date"""
    disconnects = []
    line_pattern = re.compile('jabberd/c2s.*disconnect jid=')   # how to determine relavant lines from /var/log/messages
    ip_pattern = re.compile(':([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+), port=')   # how to find IP on the line
    jid_pattern = re.compile(' jid=([^, ]+), ')   # how to find JID on the line
    for line in reversed(data['tail_n_100_var_log_messages']):
        if line_pattern.search(line):
            line_date_str = ' '.join(line.split()[0:3])
            try:
                line_date = dateutil.parser.parse(line_date_str)
            except ValueError:
                continue
            if line_date >= date:
                ip = ip_pattern.search(line).group(1)
                jid = jid_pattern.search(line).group(1)
                disconnects.append({'date': line_date, 'ip': ip, 'jid': jid})
            else:
                break
    return disconnects


def __dblog(data, date):
    """With PostgreSQL logs as an input, return relevant lines newer than provided date"""
    score = 0
    no = 0
    # Determine number of lines matching given timeframe
    for line in reversed(data):
        no += 1
        line_date_str = line.split('.')[0]
        try:
            line_date = dateutil.parser.parse(line_date_str)
        except ValueError:
            continue
        if date > line_date:
            break
    # Now try to search tracebacks we are looking for in that range - looks like this:
    #   2015-12-12 07:43:51.605 MST ERROR:  deadlock detected
    #   2015-12-12 07:43:51.605 MST DETAIL:  Process 6062 waits for ShareLock on transaction 68967950; blocked by process 27571.
    #   	Process 27571 waits for ShareLock on transaction 68967951; blocked by process 6062.
    #   	Process 6062: 
    #   	        update rhnPushClient
    #   	           set state_id = 2,
    #   	               last_ping_time = NULL,
    #   	               next_action_time = NULL
    #   	         where jabber_id = 'osad-1b19dbd0b7@example.com/osad'
    #   	    
    #   	Process 27571: 
    #   	    update rhnPushClient
    #   	       set jabber_id = 'osad-1b19dbd0b7@example.com/osad',
    #   	           next_action_time = NULL,
    #   	           last_ping_time = NULL
    #   	     where server_id = 1000011101
    #   	
    #   2015-12-12 07:43:51.605 MST HINT:  See server log for query details.
    #   2015-12-12 07:43:51.605 MST STATEMENT:  
    #   	        update rhnPushClient
    #   	           set state_id = 2,
    #   	               last_ping_time = NULL,
    #   	               next_action_time = NULL
    #   	         where jabber_id = 'osad-1b19dbd0b7@example.com/osad'
    in_traceback = False
    in_traceback_detail = False
    for line in data[-no:]:
        if 'ERROR:  deadlock detected' in line:
            in_traceback = True
            in_traceback_detail = False
            continue
        if not in_traceback:
            continue
        if 'DETAIL:  Process' in line:
            in_traceback_detail = True
            continue
        if not in_traceback_detail:
            continue
        if not line.startswith("	"):
            in_traceback = False
            in_traceback_detail = False
            continue
        if 'update rhnPushClient' in line:
            score += 1
            in_traceback = False
            in_traceback_detail = False
            continue
    return score


def indicator_dblog84(data, date):
    return __dblog(data['pgsql84_logs'], date)


def indicator_dblog92(data, date):
    return __dblog(data['pgsql92_logs'], date)


def satellite_version(data):
    return util.satellite5_version(data['installed-rpms'])


def satellite_is_emb_pg(data):
    return util.satellite5_is_emb_pg(data['rhn_conf'])


def main(data):
    score_disconnects = 0
    score_deadlocks = 0
    example_jid = None
    example_ips = []

    date = get_current_time(data)
    date = date - datetime.timedelta(0, INTERVAL * 3600)
    disconnects = indicator_syslog(data, date)
    if satellite_is_emb_pg(data):
        ver = satellite_version(data).split('.')
        assert ver[0] == '5'
        if ver[1] == '6':
            score_deadlocks = indicator_dblog84(data, date)
        if int(ver[1]) >= 7:
            score_deadlocks = indicator_dblog92(data, date)

    # Get all unique JIDs
    jids = []
    for i in disconnects:
        if i['jid'] not in jids:
            jids.append(i['jid'])

    # Check that multiple IPs are not trying to use single JID
    for jid in jids:
        ips = []
        for i in [ i for i in disconnects if i['jid'] == jid ]:
            # If we still did not seen any IP, just add first one
            if len(ips) == 0:
                ips.append(i['ip'])
                continue
            # If we have seen than one IP already, but after we have seen it we have seen different one, log error
            if i['ip'] in ips and i['ip'] != ips[-1]:
                score_disconnects += 1
                if example_jid == None and example_ips == []:
                    example_jid = jid
                    example_ips = ips
                break
            # If we got here and we have not seen the IP, just add it
            if i['ip'] not in ips:
                ips.append(i['ip'])

    if score_disconnects + score_deadlocks > 0:
        return {'score_disconnects': score_disconnects, 'example_jid': example_jid, 'example_ips': example_ips, 'score_deadlocks': score_deadlocks}


def text(result):
  out = "We have checked for signs on this Satellite 5 server that there are some\n"
  out += "OSAD clients disconnects in last %s hours and found these warning signs:\n" % INTERVAL
  if result['score_disconnects'] > 0:
      out += "  There were %s JIDs switching IPs too quickly which might indicate an issue.\n" % result['score_disconnects']
      out += "  E.g. OSAD clients from IPs %s called to Satellite with same JID %s\n" % (', '.join(result['example_ips']), result['example_jid'])
  if result['score_deadlocks'] > 0:
      out += "  There were %s deadlocks featuring 'rhnPushClient' in DB log\n" % result['score_deadlocks']
  out += "See https://access.redhat.com/solutions/337003"
  return out
