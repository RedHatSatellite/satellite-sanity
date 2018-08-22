#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

tags = ['Satellite_6']
name = 'Ensure that hammer sees all the services as running'

def main(data):
    def check_status_response(status, response, service, failed_services):
        if service != None:
            if status == None or response == None:
                failed_services.add(service)
        return failed_services

    expected_services = ('candlepin', 'candlepin_auth', 'pulp', 'pulp_auth', 'foreman_tasks')
    seen_services = set()
    failed_services = set()   # not a list to keep this unique
    service = None
    status = None
    response = None
    for row in data['hammer_ping']:
        # Looks like we are entering new service section
        m = re.search('^([a-z_]*):\s*$', row)
        if m:
            # Ensure we have properly loaded status and response for service
            # we have just processed
            failed_services = check_status_response(status, response, service, failed_services)
            service = m.group(1)
            status = None
            response = None
            seen_services.add(service)
            continue
        m = re.search('^\s*Status:\s*(.+)\s*$', row)
        if m:
            status = m.group(1)
            if status != 'ok':
                failed_services.add(service)
            continue
        m = re.search('^\s*Server Response:\s*(.*)\s*$', row)
        if m:
            response = m.group(1)
            if not re.match('^Duration: [0-9]+m?s$', response):
                failed_services.add(service)
            continue
    # Ensure we have correct status and response for last service
    failed_services = check_status_response(status, response, service, failed_services)
    # Check that we have seen all the services
    for s in expected_services:
        if s not in seen_services:
            failed_services.add(s)
    for s in seen_services:
        if s not in expected_services:
            failed_services.add(s)
    if len(failed_services) > 0:
        return {'failed_services': failed_services}

def text(result):
    return "You have %s services hammer can not reach:\n" % len(result['failed_services']) \
           + "  %s\n" % ' ,'.join(result['failed_services'])\
           + "See https://access.redhat.com/solutions/1517513"
