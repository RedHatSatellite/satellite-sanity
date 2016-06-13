#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat5_diskspace_check

class TestSat5DiskspaceCheck(unittest.TestCase):

    def test_satellite_version(self):
        input_data = {'installed-rpms': ["bash-4.1.2-33.el6_7.1.x86_64", "satellite-schema-5.7.0.20-1.el6sat.noarch", "kernel-2.6.32-573.8.1.el6.x86_64"]}
        self.assertEqual('5.7.0.20-1.el6sat.noarch', sat5_diskspace_check.satellite_version(input_data))
        input_data = {'installed-rpms': ["bash-4.1.2-33.el6_7.1.x86_64", "satellite-schema-5.6.0.1-1.el6sat.noarch", "kernel-2.6.32-573.8.1.el6.x86_64"]}
        self.assertEqual('5.6.0.1-1.el6sat.noarch', sat5_diskspace_check.satellite_version(input_data))
        input_data = {'installed-rpms': ["bash-4.1.2-33.el6_7.1.x86_64", "kernel-2.6.32-573.8.1.el6.x86_64"]}
        self.assertEqual(None, sat5_diskspace_check.satellite_version(input_data))

    def test_satellite_is_emb_pg(self):
        input_data = {'rhn_conf': ["db_backend = postgresql", "db_host = "]}
        self.assertTrue(sat5_diskspace_check.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': ["db_backend = postgresql", "db_host = external-db.example.com"]}
        self.assertFalse(sat5_diskspace_check.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': ["db_backend = oracle", "db_host = "]}
        self.assertFalse(sat5_diskspace_check.satellite_is_emb_pg(input_data))
        input_data = {'rhn_conf': ["db_backend = oracle", "db_host = external-db.example.com"]}
        self.assertFalse(sat5_diskspace_check.satellite_is_emb_pg(input_data))

    def test_var_cache_rhn(self):
        input_data = {'df_Pk_var_cache_rhn': ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_root   154687468 52989616  93839460      37% /"]}
        expected = {'required': 1048576, 'have': ['/dev/mapper/vg_dhcp131222-lv_root', 154687468, 52989616, 93839460, 37, '/'], 'desc': 'cache'}
        self.assertEqual(expected, sat5_diskspace_check.var_cache_rhn(input_data))

    def test_var_satellite(self):
        input_data = {'df_Pk_var_satellite': ["Filesystem                        1024-blocks      Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_data   515930552 172570928 317151884      36% /var/satellite"]}
        expected = {'required': 1048576, 'have': ['/dev/mapper/vg_dhcp131222-lv_data', 515930552, 172570928, 317151884, 36, '/var/satellite'], 'desc': '/var/satellite'}
        self.assertEqual(expected, sat5_diskspace_check.var_satellite(input_data))

    def test_var_lib_pgsql_data_570(self):
        input_data = {}
        input_data['installed-rpms'] = ["satellite-schema-5.7.0.20-1.el6sat.noarch"]
        input_data['rhn_conf'] = ["db_backend = postgresql", "db_host = "]
        input_data['df_Pk_opt_rh_postgresql92_root_var_lib_pgsql_data'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_psql   103081248 18588236  79250132      19% /opt/rh/postgresql92/root/var/lib/pgsql"]
        expected = {'required': 1048576, 'have': ['/dev/mapper/vg_dhcp131222-lv_psql', 103081248, 18588236, 79250132, 19, '/opt/rh/postgresql92/root/var/lib/pgsql'], 'desc': 'database'}
        self.assertEqual(expected, sat5_diskspace_check.var_lib_pgsql_data(input_data))

    def test_var_lib_pgsql_data_560(self):
        input_data = {}
        input_data['installed-rpms'] = ["satellite-schema-5.6.0.1-1.el6sat.noarch"]
        input_data['rhn_conf'] = ["db_backend = postgresql", "db_host = "]
        input_data['df_Pk_var_lib_pgsql_data'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_psql   103081248 18588236  79250132      19% /var/lib/pgsql"]
        expected = {'required': 1048576, 'have': ['/dev/mapper/vg_dhcp131222-lv_psql', 103081248, 18588236, 79250132, 19, '/var/lib/pgsql'], 'desc': 'database'}
        self.assertEqual(expected, sat5_diskspace_check.var_lib_pgsql_data(input_data))

    def test_var_lib_pgsql_data_nosat(self):
        input_data = {}
        input_data['installed-rpms'] = ["kernel-4.2.6-300.fc23.x86_64"]
        input_data['rhn_conf'] = ''
        input_data['df_Pk_var_lib_pgsql_data'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_psql   103081248 18588236  79250132      19% /var/lib/pgsql"]
        expected = None
        self.assertEqual(expected, sat5_diskspace_check.var_lib_pgsql_data(input_data))

    def test_main_nomatch(self):
        input_data = {}
        input_data['installed-rpms'] = ["satellite-schema-5.7.0.20-1.el6sat.noarch"]
        input_data['rhn_conf'] = ["db_backend = postgresql", "db_host = "]
        input_data['df_Pk_var_cache_rhn'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_root   154687468 52989616  93839460      37% /"]
        input_data['df_Pk_var_satellite'] = ["Filesystem                        1024-blocks      Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_data   515930552 172570928 317151884      36% /var/satellite"]
        input_data['df_Pk_opt_rh_postgresql92_root_var_lib_pgsql_data'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_psql   103081248 18588236  79250132      19% /opt/rh/postgresql92/root/var/lib/pgsql"]
        self.assertEqual(None, sat5_diskspace_check.main(input_data))

    def test_main_match(self):
        input_data = {}
        input_data['installed-rpms'] = ["satellite-schema-5.7.0.20-1.el6sat.noarch"]
        input_data['rhn_conf'] = ["db_backend = postgresql", "db_host = "]
        input_data['df_Pk_var_cache_rhn'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_root   154687468 146829076 0      100% /"]
        input_data['df_Pk_var_satellite'] = ["Filesystem                        1024-blocks      Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_data   515930552 172570928 317151884      36% /var/satellite"]
        input_data['df_Pk_opt_rh_postgresql92_root_var_lib_pgsql_data'] = ["Filesystem                        1024-blocks     Used Available Capacity Mounted on","/dev/mapper/vg_dhcp131222-lv_psql   103081248 18588236  79250132      19% /opt/rh/postgresql92/root/var/lib/pgsql"]
        expected = {'VOLUMES': {'/dev/mapper/vg_dhcp131222-lv_root': {'avail': 0, 'what': ['cache'], 'required': 1048576, 'size': 154687468}}}
        self.assertEqual(expected, sat5_diskspace_check.main(input_data))
