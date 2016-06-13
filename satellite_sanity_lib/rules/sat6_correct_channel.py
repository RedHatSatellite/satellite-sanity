#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_6', 'Satellite_6_preinst']
name = 'RHEL release should match Satellite 6 requirements'

def main(data):
    assert len(data['rhsm_release_show']) == 1
    if data['rhsm_release_show'][0].startswith('This system is not yet registered.'):
        return {'msg': "You are not registered using subscription-manager"}
    if data['rhsm_release_show'][0].startswith('Release: '):
        allowed = ('6Server', '7Server')
        release = data['rhsm_release_show'][0].split(": ")[1]
        if release not in allowed:
            return {'msg': "Your release is set to %s, but should be one of %s" % (release, ", ".join(allowed))}

def text(result):
    return "Your subscription-manager registration doesn't match Satellite 6 requirements:\n"\
           + result['msg'] + "\n"\
           + "See https://access.redhat.com/documentation/en-US/Red_Hat_Satellite/6.1/html/Installation_Guide/sect-Red_Hat_Satellite-Installation_Guide-Prerequisites.html#sect-Red_Hat_Satellite-Installation_Guide-Prerequisites-Base_Operating_System"
