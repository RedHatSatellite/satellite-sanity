#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat5_cobbler_config

HOSTNAME = ['satellite.example.com']

etc_cobbler_settings_redhat_management_type = 'redhat_management_type: "site"'
etc_cobbler_settings_redhat_management_server = 'redhat_management_server: "satellite.example.com"'
etc_cobbler_settings_server = 'server: satellite.example.com'
etc_cobbler_modules_conf_authentication_module = 'module = authn_spacewalk'
etc_cobbler_settings_redhat_management_type_failing = 'redhat_management_type: default'
etc_cobbler_settings_redhat_management_server_failing = 'redhat_management_server: localhost'
etc_cobbler_settings_server_failing = 'server: localhost'
etc_cobbler_modules_conf_authentication_module_failing = 'module = default'

ETC_COBBLER_CONFIG_TEMPLATE = """---
allow_duplicate_hostnames: 0

allow_duplicate_ips: 0

allow_duplicate_macs: 0

anamon_enabled: 0

build_reporting_enabled: 0
build_reporting_sender: ""
build_reporting_email: [ 'root@localhost' ]
build_reporting_smtp_server: "localhost"
build_reporting_subject: ""

cheetah_import_whitelist:
   - "random"
   - "re"
   - "time"

createrepo_flags: "-c cache -s sha"

default_kickstart: /var/lib/cobbler/kickstarts/default.ks

default_name_servers: []

default_ownership:
    - "admin"

default_password_crypted: "$1$mF86/UHC$WvcIcX2t6crBz2onWxyac."

default_virt_bridge: xenbr0

default_virt_file_size: 5

default_virt_ram: 512

default_virt_type: xenpv

enable_menu: 1

func_auto_setup: 0
func_master: overlord.example.org

http_port: 80

kernel_options:
    ksdevice: bootif
    lang: ' '
    text: ~

kernel_options_s390x:
    RUNKS: 1
    ramdisk_size: 40000
    root: /dev/ram0
    ro: ~
    ip: off
    vnc: ~

ldap_server: "ldap.example.com"
ldap_base_dn: "DC=example,DC=com"
ldap_port: 389
ldap_tls: 1
ldap_anonymous_bind: 1
ldap_search_bind_dn: ''
ldap_search_passwd: ''
ldap_search_prefix: 'uid='

mgmt_classes: []
mgmt_parameters:
   from_cobbler: 1

manage_dhcp: 0

manage_dns: 0

manage_forward_zones: []
manage_reverse_zones: []

next_server: satellite.example.com

power_management_default_type: 'ipmitool'

power_template_dir: "/etc/cobbler/power"

pxe_just_once: 1

pxe_template_dir: "/etc/cobbler/pxe"

%s

%s

redhat_management_key: ""

redhat_management_permissive: 0

register_new_installs: 0

reposync_flags: "-l -m -d"

restart_dns: 1
restart_dhcp: 1

run_install_triggers: 1

scm_track_enabled: 0
scm_track_mode: "git"

%s

snippetsdir: /var/lib/cobbler/snippets

template_remote_kickstarts: 0

virt_auto_boot: 1

webdir: /var/www/cobbler

xmlrpc_port: 25151

yum_post_install_mirror: 1

yum_distro_priority: 1

yumdownloader_flags: "--resolve"

safe_templating: true"""
ETC_COBBLER_MODULES_CONF_TEMPLATE = """

[authentication]
%s



[authorization]
module = authz_allowall


[dns]
module = manage_bind

  
[dhcp]
module = manage_isc

"""

ETC_COBBLER_CONFIG_CORRECT = ETC_COBBLER_CONFIG_TEMPLATE % (etc_cobbler_settings_redhat_management_type, etc_cobbler_settings_redhat_management_server, etc_cobbler_settings_server)
ETC_COBBLER_CONFIG_FAILING = ETC_COBBLER_CONFIG_TEMPLATE % (etc_cobbler_settings_redhat_management_type_failing, etc_cobbler_settings_redhat_management_server_failing, etc_cobbler_settings_server_failing)
ETC_COBBLER_CONFIG_FAILING_ONE = ETC_COBBLER_CONFIG_TEMPLATE % (etc_cobbler_settings_redhat_management_type, etc_cobbler_settings_redhat_management_server_failing, etc_cobbler_settings_server)
ETC_COBBLER_CONFIG_MISSING = ETC_COBBLER_CONFIG_TEMPLATE % ('', '', '')
ETC_COBBLER_CONFIG_NOQUOT = ETC_COBBLER_CONFIG_TEMPLATE % (etc_cobbler_settings_redhat_management_type.replace('"', ''), etc_cobbler_settings_redhat_management_server.replace('"', ''), etc_cobbler_settings_server)
ETC_COBBLER_MODULES_CONF_CORRECT = ETC_COBBLER_MODULES_CONF_TEMPLATE % (etc_cobbler_modules_conf_authentication_module)
ETC_COBBLER_MODULES_CONF_FAILING = ETC_COBBLER_MODULES_CONF_TEMPLATE % (etc_cobbler_modules_conf_authentication_module_failing)
ETC_COBBLER_MODULES_CONF_MISSING = ETC_COBBLER_MODULES_CONF_TEMPLATE % ('')
ETC_COBBLER_MODULES_CONF_NOQUOT = ETC_COBBLER_MODULES_CONF_CORRECT

ETC_COBBLER_CONFIG_CORRECT = ETC_COBBLER_CONFIG_CORRECT.split("\n")
ETC_COBBLER_CONFIG_FAILING = ETC_COBBLER_CONFIG_FAILING.split("\n")
ETC_COBBLER_CONFIG_FAILING_ONE = ETC_COBBLER_CONFIG_FAILING_ONE.split("\n")
ETC_COBBLER_CONFIG_MISSING = ETC_COBBLER_CONFIG_MISSING.split("\n")
ETC_COBBLER_CONFIG_NOQUOT = ETC_COBBLER_CONFIG_NOQUOT.split("\n")
ETC_COBBLER_MODULES_CONF_CORRECT = ETC_COBBLER_MODULES_CONF_CORRECT.split("\n")
ETC_COBBLER_MODULES_CONF_FAILING = ETC_COBBLER_MODULES_CONF_FAILING.split("\n")
ETC_COBBLER_MODULES_CONF_MISSING = ETC_COBBLER_MODULES_CONF_MISSING.split("\n")
ETC_COBBLER_MODULES_CONF_NOQUOT = ETC_COBBLER_MODULES_CONF_NOQUOT.split("\n")

class TestSat5CobblerConfig(unittest.TestCase):

    def test_match(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_FAILING
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_FAILING
        expected = {'errors': [
            'In /etc/cobbler/settings there should be \'redhat_management_type: "site"\'',
            'In /etc/cobbler/settings there should be \'redhat_management_server: satellite.example.com\'',
            "In /etc/cobbler/settings there should be 'server: satellite.example.com'",
            "In /etc/cobbler/modules.conf there should be 'module = authn_spacewalk'"
        ]}
        self.assertEquals(expected, sat5_cobbler_config.main(input_data))

    def test_match_one(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_FAILING_ONE
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_CORRECT
        expected = {'errors': [
            'In /etc/cobbler/settings there should be \'redhat_management_server: satellite.example.com\''
        ]}
        self.assertEquals(expected, sat5_cobbler_config.main(input_data))

    def test_match_missing(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_MISSING
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_MISSING
        expected = {'errors': [
            'Not all of redhat_management_type, redhat_management_server and server options found in /etc/cobbler/settings',
            'Option module in section authentication not found in /etc/cobbler/modules.conf'
        ]}
        self.assertEquals(expected, sat5_cobbler_config.main(input_data))

    def test_match_missing(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_CORRECT
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_MISSING
        expected = {'errors': [
            'Option module in section authentication not found in /etc/cobbler/modules.conf'
        ]}
        self.assertEquals(expected, sat5_cobbler_config.main(input_data))

    def test_no_match(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_CORRECT
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_CORRECT
        self.assertEquals(None, sat5_cobbler_config.main(input_data))

    def test_no_match_noquot(self):
        input_data = {}
        input_data['hostname'] = HOSTNAME
        input_data['etc_cobbler_settings'] = ETC_COBBLER_CONFIG_NOQUOT
        input_data['etc_cobbler_modules_conf'] = ETC_COBBLER_MODULES_CONF_NOQUOT
        self.assertEquals(None, sat5_cobbler_config.main(input_data))
