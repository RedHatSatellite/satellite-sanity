#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity.rules import sat5_rhn_charsets

CORRECT_PG = """ server_encoding 
-----------------
 UTF8
(1 row)

 client_encoding 
-----------------
 UTF8
(1 row)
""".split("\n")
CORRECT_ORA = """
PARAMETER		       VALUE
------------------------------ ------------------------------------------------------------------------------------------------------------------------
NLS_CHARACTERSET	       UTF8
NLS_NCHAR_CHARACTERSET	       UTF8

""".split("\n")

INCORRECT_PG = """ server_encoding 
-----------------
 LATIN9
(1 row)

 client_encoding 
-----------------
 LATIN9
(1 row)
""".split("\n")
INCORRECT_ORA = """
PARAMETER                      VALUE
------------------------------ ----------------------------------------
NLS_CHARACTERSET               WE8ISO8859P1
NLS_NCHAR_CHARACTERSET         AL16UTF16
""".split("\n")

RHNCONF_ORA = """db_backend = oracle
db_user = rhnsat
db_password = rhnsat
db_name = //oracle.example.com:1522/rhnsat.world
db_host = oracle.example.com
db_port = 1522
db_ssl_enabled = """.split("\n")
RHNCONF_PG = """db_backend = postgresql
db_user = rhnuser
db_password = rhnpw
db_name = rhnschema
db_host = 
db_port = 
db_ssl_enabled = """.split("\n")

class TestSat5RhnCharsets(unittest.TestCase):

    def test_match_pg(self):
        input_data = {'rhn_charsets': INCORRECT_PG, 'rhn_conf': RHNCONF_PG}
        expected = {'db_first': 'LATIN9', 'db_second': 'LATIN9'}
        self.assertEqual(expected, sat5_rhn_charsets.main(input_data))

    def test_no_match_pg(self):
        input_data = {'rhn_charsets': CORRECT_PG, 'rhn_conf': RHNCONF_PG}
        self.assertEqual(None, sat5_rhn_charsets.main(input_data))

    def test_match_ora(self):
        input_data = {'rhn_charsets': INCORRECT_ORA, 'rhn_conf': RHNCONF_ORA}
        expected = {'db_first': 'WE8ISO8859P1', 'db_second': 'AL16UTF16'}
        self.assertEqual(expected, sat5_rhn_charsets.main(input_data))

    def test_no_match_ora(self):
        input_data = {'rhn_charsets': CORRECT_ORA, 'rhn_conf': RHNCONF_PG}
        self.assertEqual(None, sat5_rhn_charsets.main(input_data))
