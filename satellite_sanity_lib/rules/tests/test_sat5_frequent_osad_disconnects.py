#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import datetime

from satellite_sanity_lib.rules import sat5_frequent_osad_disconnects

YEAR = datetime.datetime.now().year

SYSLOG_CORRECT = """Mar 14 13:26:50 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 14 13:27:04 satellite dhclient[1367]: DHCPREQUEST on eth0 to 255.255.255.255 port 67 (xid=0x58995fab)
Mar 14 13:27:04 satellite dhclient[1367]: DHCPACK from 10.35.131.253 (xid=0x58995fab)
Mar 14 13:27:06 satellite dhclient[1367]: bound to 10.35.130.126 -- renewal in 40971 seconds.
Mar 14 17:39:16 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.49.97, port=46447] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 1326
Mar 14 17:39:17 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 19:04:34 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.48.12, port=48715] connect
Mar 14 19:04:35 satellite jabberd/c2s[10811]: [10] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 14 19:04:35 satellite jabberd/c2s[10811]: [10] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 19:04:35 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 19:23:29 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.48.12, port=48715] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 14 19:23:30 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 23:02:58 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.48.12, port=48720] connect
Mar 14 23:03:00 satellite jabberd/c2s[10811]: [10] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 14 23:03:00 satellite jabberd/c2s[10811]: [10] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 23:03:00 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 14 23:23:20 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.48.12, port=48720] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 8
Mar 14 23:23:20 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 00:49:57 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 00:50:03 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 00:50:16 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:37:24 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:37:37 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:37:57 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:38:04 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:38:08 satellite jabberd/c2s[10811]: [10] [::ffff:10.9.48.12, port=48734] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 04:38:09 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 04:38:24 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:38:45 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 04:38:58 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:08:20 satellite jabberd/sm[10802]: session started: jid=osad-06386d3502@satellite.example.com/osad
Mar 15 07:08:23 satellite jabberd/c2s[10811]: [16] [::ffff:10.35.130.126, port=35929] connect
Mar 15 07:08:28 satellite jabberd/c2s[10811]: [16] legacy authentication succeeded: host=, username=rhn-dispatcher-sat, resource=superclient, TLS negotiated
Mar 15 07:08:28 satellite jabberd/c2s[10811]: [16] requesting session: jid=rhn-dispatcher-sat@satellite.example.com/superclient
Mar 15 07:08:28 satellite jabberd/c2s[10811]: [7] [::ffff:10.35.130.126, port=35078] disconnect jid=rhn-dispatcher-sat@satellite.example.com/superclient, packets: 129155
Mar 15 07:08:28 satellite jabberd/sm[10802]: session replaced: jid=rhn-dispatcher-sat@satellite.example.com/superclient
Mar 15 07:08:30 satellite jabberd/s2s[10820]: dns lookup for dns.example.com failed
Mar 15 07:08:36 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:08:54 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:27:28 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:27:48 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:27:59 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:28:10 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:28:22 satellite jabberd/c2s[10811]: [10] [::ffff:10.17.64.86, port=47286] disconnect jid=osad-6fb988741e@satellite.example.com/osad, packets: 26
Mar 15 07:28:23 satellite jabberd/c2s[10811]: [11] [::ffff:10.17.64.86, port=48409] disconnect jid=osad-01f62470a3@satellite.example.com/osad, packets: 26
Mar 15 07:28:23 satellite jabberd/c2s[10811]: [12] [::ffff:10.17.64.86, port=48545] disconnect jid=osad-b1f87862c8@satellite.example.com/osad, packets: 26
Mar 15 07:28:23 satellite jabberd/c2s[10811]: [13] [::ffff:10.17.64.86, port=48875] disconnect jid=osad-ceecf22599@satellite.example.com/osad, packets: 29
Mar 15 07:28:23 satellite jabberd/c2s[10811]: [14] [::ffff:10.17.64.86, port=49889] disconnect jid=osad-2b294f5c35@satellite.example.com/osad, packets: 36
Mar 15 07:28:23 satellite jabberd/sm[10802]: session ended: jid=osad-6fb988741e@satellite.example.com/osad
Mar 15 07:28:23 satellite jabberd/sm[10802]: session ended: jid=osad-01f62470a3@satellite.example.com/osad
Mar 15 07:28:23 satellite jabberd/sm[10802]: session ended: jid=osad-b1f87862c8@satellite.example.com/osad
Mar 15 07:28:23 satellite jabberd/sm[10802]: session ended: jid=osad-ceecf22599@satellite.example.com/osad
Mar 15 07:28:23 satellite jabberd/sm[10802]: session ended: jid=osad-2b294f5c35@satellite.example.com/osad
Mar 15 07:28:24 satellite jabberd/c2s[10811]: [15] [::ffff:10.17.64.86, port=49992] disconnect jid=osad-06386d3502@satellite.example.com/osad, packets: 13
Mar 15 07:28:24 satellite jabberd/sm[10802]: session ended: jid=osad-06386d3502@satellite.example.com/osad
Mar 15 07:28:26 satellite jabberd/c2s[10811]: [17] [::ffff:10.17.64.86, port=50294] disconnect jid=osad-3358eaf2b5@satellite.example.com/osad, packets: 21
Mar 15 07:28:26 satellite jabberd/sm[10802]: session ended: jid=osad-3358eaf2b5@satellite.example.com/osad
Mar 15 07:28:27 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:28:28 satellite jabberd/c2s[10811]: [7] [::ffff:10.17.64.86, port=50107] disconnect jid=osad-6c4322fa9a@satellite.example.com/osad, packets: 21
Mar 15 07:28:28 satellite jabberd/sm[10802]: session ended: jid=osad-6c4322fa9a@satellite.example.com/osad
Mar 15 07:28:41 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:28:48 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 07:29:02 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 10:57:00 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48739] connect
Mar 15 10:57:02 satellite jabberd/c2s[10811]: [7] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 15 10:57:02 satellite jabberd/c2s[10811]: [7] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 10:57:02 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 11:19:41 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48739] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 11:19:41 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 12:23:54 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48742] connect
Mar 15 12:23:55 satellite jabberd/c2s[10811]: [7] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 15 12:23:55 satellite jabberd/c2s[10811]: [7] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 12:23:55 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 12:40:04 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48742] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 12:40:04 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 13:39:41 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48746] connect
Mar 15 13:39:42 satellite jabberd/c2s[10811]: [7] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 15 13:39:42 satellite jabberd/c2s[10811]: [7] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 13:39:42 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 14:03:03 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48746] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 14:03:03 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 14:21:44 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48749] connect
Mar 15 14:21:45 satellite jabberd/c2s[10811]: [7] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 15 14:21:45 satellite jabberd/c2s[10811]: [7] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 14:21:46 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 14:49:07 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48749] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 14:49:07 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 18:51:09 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48755] connect
Mar 15 18:51:10 satellite jabberd/c2s[10811]: [7] legacy authentication succeeded: host=, username=osad-3de354aec4, resource=osad, TLS negotiated
Mar 15 18:51:10 satellite jabberd/c2s[10811]: [7] requesting session: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 18:51:10 satellite jabberd/sm[10802]: session started: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 19:16:09 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48755] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 15 19:16:09 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 21:11:05 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 21:11:09 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 21:11:17 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:35:44 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:35:53 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:36:01 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:36:11 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:36:19 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48760] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 8
Mar 15 23:36:19 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 15 23:36:20 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:36:39 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 15 23:36:54 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:10:18 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:10:32 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:10:51 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:11:12 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:11:14 satellite jabberd/c2s[10811]: [7] [::ffff:10.9.48.12, port=48792] disconnect jid=osad-3de354aec4@satellite.example.com/osad, packets: 6
Mar 16 01:11:15 satellite jabberd/sm[10802]: session ended: jid=osad-3de354aec4@satellite.example.com/osad
Mar 16 01:11:23 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:11:37 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)
Mar 16 01:11:58 satellite dhclient[1367]: DHCPREQUEST on eth0 to 10.39.5.26 port 67 (xid=0x58995fab)""".split("\n")
SYSLOG_WRONG = """Mar 15 12:35:07 satellite jabberd/c2s[31237]: [7] [::ffff:192.168.29.1, port=40802] connect
Mar 15 12:35:07 satellite jabberd/c2s[31237]: [7] legacy authentication succeeded: host=, username=osad-fc2a194137, resource=osad, TLS negotiated
Mar 15 12:35:07 satellite jabberd/c2s[31237]: [7] requesting session: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:35:08 satellite jabberd/sm[31230]: session started: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:36:30 satellite jabberd/c2s[31237]: [10] [::ffff:192.168.29.2, port=51381] connect
Mar 15 12:36:30 satellite jabberd/c2s[31237]: [10] legacy authentication succeeded: host=, username=osad-fc2a194137, resource=osad, TLS negotiated
Mar 15 12:36:30 satellite jabberd/c2s[31237]: [10] requesting session: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:36:30 satellite jabberd/c2s[31237]: [7] [::ffff:192.168.29.1, port=40802] disconnect jid=osad-fc2a194137@satellite.example.com/osad, packets: 6
Mar 15 12:36:30 satellite jabberd/sm[31230]: session replaced: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:36:45 satellite jabberd/c2s[31237]: [7] [::ffff:192.168.29.3, port=57149] connect
Mar 15 12:36:45 satellite jabberd/c2s[31237]: [7] legacy authentication succeeded: host=, username=osad-fc2a194137, resource=osad, TLS negotiated
Mar 15 12:36:45 satellite jabberd/c2s[31237]: [7] requesting session: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:36:45 satellite jabberd/c2s[31237]: [10] [::ffff:192.168.29.2, port=51381] disconnect jid=osad-fc2a194137@satellite.example.com/osad, packets: 6
Mar 15 12:36:45 satellite jabberd/sm[31230]: session replaced: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:38:03 satellite jabberd/c2s[31237]: [10] [::ffff:192.168.29.1, port=40804] connect
Mar 15 12:38:03 satellite jabberd/c2s[31237]: [10] legacy authentication succeeded: host=, username=osad-fc2a194137, resource=osad, TLS negotiated
Mar 15 12:38:03 satellite jabberd/c2s[31237]: [10] requesting session: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:38:03 satellite jabberd/c2s[31237]: [7] [::ffff:192.168.29.3, port=57149] disconnect jid=osad-fc2a194137@satellite.example.com/osad, packets: 6
Mar 15 12:38:03 satellite jabberd/sm[31230]: session replaced: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:39:30 satellite jabberd/c2s[31237]: [10] [::ffff:192.168.29.2, port=51381] connect
Mar 15 12:39:30 satellite jabberd/c2s[31237]: [10] legacy authentication succeeded: host=, username=osad-fc2a194137, resource=osad, TLS negotiated
Mar 15 12:39:30 satellite jabberd/c2s[31237]: [10] requesting session: jid=osad-fc2a194137@satellite.example.com/osad
Mar 15 12:39:30 satellite jabberd/c2s[31237]: [7] [::ffff:192.168.29.1, port=40802] disconnect jid=osad-fc2a194137@satellite.example.com/osad, packets: 6
Mar 15 12:39:30 satellite jabberd/sm[31230]: session replaced: jid=osad-fc2a194137@satellite.example.com/osad""".split("\n")

# With this date we should get all issues from our logs here
START_DATE = datetime.datetime(YEAR, 3, 15, 2, 0, 0)
START_DATE_STR = START_DATE.strftime("%c")
# Even when looking 3 days back in the logs, there should be no relevant loge entries in this date range
START_DATE_CLEAN = datetime.datetime(YEAR, 3, 20, 0, 0, 0)
START_DATE_CLEAN_STR = START_DATE_CLEAN.strftime("%c")

DB84LOG_CORRECT = """""".split("\n")
DB92LOG_CORRECT = """2016-03-18 01:51:58.795 EDT WARNING:  there is already a transaction in progress
2016-03-18 02:20:21.093 EDT ERROR:  -20263 : (no_subscribe_permissions) - Insufficient permissions for subscription
2016-03-18 02:20:21.093 EDT CONTEXT:  SQL statement "SELECT rhn_exception.raise_exception('no_subscribe_permissions')"
        PL/pgSQL function rhn_channel.base_channel_rel_archid(character varying,numeric,numeric,numeric) line 65 at PERFORM
        PL/pgSQL function rhn_channel.base_channel_for_release_arch(character varying,character varying,numeric,numeric) line 15 at RETURN
2016-03-18 02:20:21.093 EDT STATEMENT:  
                select ca.label arch,
                       c.id,
                       c.parent_channel,
                       c.org_id,
                       c.label,
                       c.name,
                       c.summary,
                       c.description,
                       to_char(c.last_modified, 'YYYYMMDDHH24MISS') last_modified,
                       rhn_channel.available_chan_subscriptions(c.id, '1440') available_subscriptions
                  from rhnChannel c,
                       rhnChannelArch ca
                where c.channel_arch_id = ca.id
                  and c.id = rhn_channel.base_channel_for_release_arch(
                        '5Server', 'x86_64-redhat-linux', '1440', 2378)
            
2016-03-18 02:45:18.129 EDT WARNING:  there is already a transaction in progress""".split("\n")
DB92LOG_CORRECT_START = datetime.datetime(2016, 03, 18, 0, 0, 0)
DB84LOG_WRONG = """""".split("\n")
DB92LOG_WRONG = """2016-03-15 02:47:40.120 MST WARNING:  there is already a transaction in progress
2016-03-15 02:47:41.263 MST WARNING:  there is already a transaction in progress
2016-03-15 07:43:51.605 MST ERROR:  deadlock detected
2016-03-15 07:43:51.605 MST DETAIL:  Process 6062 waits for ShareLock on transaction 68967950; blocked by process 27571.
	Process 27571 waits for ShareLock on transaction 68967951; blocked by process 6062.
	Process 6062: 
	        update rhnPushClient
	           set state_id = 2,
	               last_ping_time = NULL,
	               next_action_time = NULL
	         where jabber_id = 'osad-1b19dbd0b7@example.com/osad'
	    
	Process 27571: 
	    update rhnPushClient
	       set jabber_id = 'osad-1b19dbd0b7@example.com/osad',
	           next_action_time = NULL,
	           last_ping_time = NULL
	     where server_id = 1000011101
	
2016-03-15 07:43:51.605 MST HINT:  See server log for query details.
2016-03-15 07:43:51.605 MST STATEMENT:  
	        update rhnPushClient
	           set state_id = 2,
	               last_ping_time = NULL,
	               next_action_time = NULL
	         where jabber_id = 'osad-1b19dbd0b7@example.com/osad'
	    
2016-03-15 07:44:01.642 MST ERROR:  current transaction is aborted, commands ignored until end of transaction block
2016-03-15 07:44:01.642 MST STATEMENT:  select 1""".split("\n")
DB92LOG_WRONG_START = datetime.datetime(2016, 3, 15, 0, 0, 0)

VER_570 = "5.7.0.20-1.el6sat.noarch"
VER_560 = "5.6.0.1-1.el6sat.noarch"
INSTALLED_RPMS_570 = ["bash-4.1.2-33.el6_7.1.x86_64", "satellite-schema-%s" % VER_570, "kernel-2.6.32-573.8.1.el6.x86_64"]
INSTALLED_RPMS_560 = ["bash-4.1.2-33.el6_7.1.x86_64", "satellite-schema-%s" % VER_560, "kernel-2.6.32-573.8.1.el6.x86_64"]
INSTALLED_RPMS_NOSAT = ["bash-4.1.2-33.el6_7.1.x86_64", "kernel-2.6.32-573.8.1.el6.x86_64"]

RHN_CONF_PG_EMB = ["db_backend = postgresql", "db_host = "]
RHN_CONF_PG_EXT = ["db_backend = postgresql", "db_host = external-db.example.com"]
RHN_CONF_ORA_EMB = ["db_backend = oracle", "db_host = "]
RHN_CONF_ORA_EXT = ["db_backend = oracle", "db_host = external-db.example.com"]

DATE = 'Wed Mar 16 04:43:11 EDT 2016'
DATE_PARSED = datetime.datetime(2016, 3, 16, 4, 43, 11)

class TestSat5FrequentOsadDisconnects(unittest.TestCase):

    def test_satellite_version(self):
        input_data = {'installed-rpms': INSTALLED_RPMS_570}
        self.assertEqual(VER_570, sat5_frequent_osad_disconnects.satellite_version(input_data))
        input_data = {'installed-rpms': INSTALLED_RPMS_560}
        self.assertEqual(VER_560, sat5_frequent_osad_disconnects.satellite_version(input_data))
        input_data = {'installed-rpms': INSTALLED_RPMS_NOSAT}
        self.assertEqual(None, sat5_frequent_osad_disconnects.satellite_version(input_data))

    def test_satellite_is_emb_pg(self):
        input_data = {'rhn_conf': RHN_CONF_PG_EMB}
        self.assertTrue(sat5_frequent_osad_disconnects.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': RHN_CONF_PG_EXT}
        self.assertFalse(sat5_frequent_osad_disconnects.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': RHN_CONF_ORA_EMB}
        self.assertFalse(sat5_frequent_osad_disconnects.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': RHN_CONF_ORA_EXT}
        self.assertFalse(sat5_frequent_osad_disconnects.satellite_is_emb_pg(input_data))

    def test_get_current_time(self):
        input_data = {'date': [DATE]}
        self.assertEqual(DATE_PARSED, sat5_frequent_osad_disconnects.get_current_time(input_data))

    def test_indicator_syslog(self):
        input_data = {'tail_n_100_var_log_messages': SYSLOG_CORRECT}
        expected = [
            {'date': datetime.datetime(YEAR, 3, 16, 1, 11, 14), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 23, 36, 19), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 19, 16, 9), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 14, 49, 7), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 14, 3, 3), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 12, 40, 4), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 11, 19, 41), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 28), 'ip': '10.17.64.86', 'jid': 'osad-6c4322fa9a@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 26), 'ip': '10.17.64.86', 'jid': 'osad-3358eaf2b5@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 24), 'ip': '10.17.64.86', 'jid': 'osad-06386d3502@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 23), 'ip': '10.17.64.86', 'jid': 'osad-2b294f5c35@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 23), 'ip': '10.17.64.86', 'jid': 'osad-ceecf22599@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 23), 'ip': '10.17.64.86', 'jid': 'osad-b1f87862c8@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 23), 'ip': '10.17.64.86', 'jid': 'osad-01f62470a3@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 28, 22), 'ip': '10.17.64.86', 'jid': 'osad-6fb988741e@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 7, 8, 28), 'ip': '10.35.130.126', 'jid': 'rhn-dispatcher-sat@satellite.example.com/superclient'},
            {'date': datetime.datetime(YEAR, 3, 15, 4, 38, 8), 'ip': '10.9.48.12', 'jid': 'osad-3de354aec4@satellite.example.com/osad'}]
        self.assertEqual(expected, sat5_frequent_osad_disconnects.indicator_syslog(input_data, START_DATE))

    def test_indicator_syslog_wrong(self):
        input_data = {'tail_n_100_var_log_messages': SYSLOG_WRONG}
        expected = [
            {'date': datetime.datetime(YEAR, 3, 15, 12, 39, 30), 'ip': '192.168.29.1', 'jid': 'osad-fc2a194137@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 12, 38, 3), 'ip': '192.168.29.3', 'jid': 'osad-fc2a194137@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 12, 36, 45), 'ip': '192.168.29.2', 'jid': 'osad-fc2a194137@satellite.example.com/osad'},
            {'date': datetime.datetime(YEAR, 3, 15, 12, 36, 30), 'ip': '192.168.29.1', 'jid': 'osad-fc2a194137@satellite.example.com/osad'}]
        self.assertEqual(expected, sat5_frequent_osad_disconnects.indicator_syslog(input_data, START_DATE))

    def test_indicator_dblog(self):
        input_data= {'pgsql92_logs': DB92LOG_WRONG}
        self.assertEqual(1, sat5_frequent_osad_disconnects.indicator_dblog92(input_data, DB92LOG_WRONG_START))
        input_data= {'pgsql92_logs': DB92LOG_CORRECT}
        self.assertEqual(0, sat5_frequent_osad_disconnects.indicator_dblog92(input_data, DB92LOG_CORRECT_START))

    def test_no_match(self):
        # With no match
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_CORRECT
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_CORRECT
        self.assertEqual(None, sat5_frequent_osad_disconnects.main(input_data))
        # With start date set after issues in the logs
        input_data = {}
        input_data['date'] = [START_DATE_CLEAN_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_WRONG
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        self.assertEqual(None, sat5_frequent_osad_disconnects.main(input_data))
        # With issues in PG92 log if we are on Sat560, there should be KeyError
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_CORRECT
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_560
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        self.assertRaises(KeyError, sat5_frequent_osad_disconnects.main, input_data)
        # Even with issues in PG92 log if we are not on external PG, there should be no match
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_CORRECT
        input_data['rhn_conf'] = RHN_CONF_PG_EXT
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        self.assertEqual(None, sat5_frequent_osad_disconnects.main(input_data))
        # Even with issues in PG92 log if we are not on external Ora, there should be no match
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_CORRECT
        input_data['rhn_conf'] = RHN_CONF_ORA_EXT
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        self.assertEqual(None, sat5_frequent_osad_disconnects.main(input_data))

    def test_match(self):
        # With both wrong
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_WRONG
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        expected = {'score_disconnects': 1, 'example_jid': 'osad-fc2a194137@satellite.example.com/osad', 'example_ips': ['192.168.29.1', '192.168.29.3', '192.168.29.2'], 'score_deadlocks': 1}
        self.assertDictEqual(expected, sat5_frequent_osad_disconnects.main(input_data))
        # With only syslog
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_WRONG
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_CORRECT
        expected = {'score_disconnects': 1, 'example_jid': 'osad-fc2a194137@satellite.example.com/osad', 'example_ips': ['192.168.29.1', '192.168.29.3', '192.168.29.2'], 'score_deadlocks': 0}
        self.assertDictEqual(expected, sat5_frequent_osad_disconnects.main(input_data))
        # With only DB
        input_data = {}
        input_data['date'] = [START_DATE_STR]
        input_data['tail_n_100_var_log_messages'] = SYSLOG_CORRECT
        input_data['rhn_conf'] = RHN_CONF_PG_EMB
        input_data['installed-rpms'] = INSTALLED_RPMS_570
        input_data['pgsql92_logs'] = DB92LOG_WRONG
        expected = {'score_disconnects': 0, 'example_jid': None, 'example_ips': [], 'score_deadlocks': 1}
        self.assertDictEqual(expected, sat5_frequent_osad_disconnects.main(input_data))
