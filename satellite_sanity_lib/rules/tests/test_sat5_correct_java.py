#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from satellite_sanity_lib.rules import sat5_correct_java

ALTERNATIVES_IBM_160 = """java - status is auto.
 link currently points to /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java
/usr/lib/jvm/jre-1.5.0-gcj/bin/java - priority 1500
 slave ControlPanel: (null)
 slave javaws: (null)
 slave keytool: /usr/lib/jvm/jre-1.5.0-gcj/bin/keytool
 slave policytool: (null)
 slave rmid: (null)
 slave rmiregistry: /usr/lib/jvm/jre-1.5.0-gcj/bin/rmiregistry
 slave tnameserv: (null)
 slave jre_exports: /usr/lib/jvm-exports/jre-1.5.0-gcj
 slave jre: /usr/lib/jvm/jre-1.5.0-gcj
/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java - priority 160162
 slave ControlPanel: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel
 slave javaws: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/javaws
 slave keytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/keytool
 slave policytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/policytool
 slave rmid: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmid
 slave rmiregistry: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmiregistry
 slave tnameserv: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/tnameserv
 slave jre_exports: /usr/lib/jvm-exports/jre-1.6.0-ibm.x86_64
 slave jre: /usr/lib/jvm/jre-1.6.0-ibm.x86_64
Current `best' version is /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java.""".split("\n")
ALTERNATIVES_IBM_170 = """java - status is auto.
 link currently points to /usr/lib/jvm/jre-1.7.1-ibm.x86_64/bin/java
/usr/lib/jvm/jre-1.7.1-ibm.x86_64/bin/java - priority 170310
 slave ControlPanel: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/ControlPanel
 slave javaws: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/javaws
 slave keytool: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/keytool
 slave policytool: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/policytool
 slave rmid: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/rmid
 slave rmiregistry: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/rmiregistry
 slave tnameserv: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre/bin/tnameserv
 slave jre_exports: /usr/lib/jvm-exports/java-1.7.1-ibm-1.7.1.3.10.x86_64
 slave jre: /usr/lib/jvm/java-1.7.1-ibm-1.7.1.3.10.x86_64/jre
/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java - priority 160167
 slave ControlPanel: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel
 slave javaws: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/javaws
 slave keytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/keytool
 slave policytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/policytool
 slave rmid: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmid
 slave rmiregistry: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmiregistry
 slave tnameserv: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/tnameserv
 slave jre_exports: /usr/lib/jvm-exports/jre-1.6.0-ibm.x86_64
 slave jre: /usr/lib/jvm/jre-1.6.0-ibm.x86_64
Current `best' version is /usr/lib/jvm/jre-1.7.1-ibm.x86_64/bin/java.""".split("\n")
ALTERNATIVE_IBM_170 = "/usr/lib/jvm/jre-1.7.1-ibm.x86_64/bin/java"
ALTERNATIVES_OPENJDK = """java - status is auto.
 link currently points to /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/java
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/java - priority 1851
 slave jre: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre
 slave jre_exports: /usr/lib/jvm-exports/jre-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64
 slave jjs: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/jjs
 slave keytool: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/keytool
 slave orbd: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/orbd
 slave pack200: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/pack200
 slave rmid: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/rmid
 slave rmiregistry: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/rmiregistry
 slave servertool: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/servertool
 slave tnameserv: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/tnameserv
 slave unpack200: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/unpack200
 slave java.1.gz: /usr/share/man/man1/java-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave jjs.1.gz: /usr/share/man/man1/jjs-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave policytool: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/policytool
 slave keytool.1.gz: /usr/share/man/man1/keytool-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave orbd.1.gz: /usr/share/man/man1/orbd-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave pack200.1.gz: /usr/share/man/man1/pack200-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave rmid.1.gz: /usr/share/man/man1/rmid-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave rmiregistry.1.gz: /usr/share/man/man1/rmiregistry-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave servertool.1.gz: /usr/share/man/man1/servertool-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave tnameserv.1.gz: /usr/share/man/man1/tnameserv-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
 slave unpack200.1.gz: /usr/share/man/man1/unpack200-java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64.1.gz
Current `best' version is /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/java.""".split("\n")
ALTERNATIVE_OPENJDK = "/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.51-1.b16.el6_7.x86_64/jre/bin/java"
ALTERNATIVES_NONE = "".split("\n")   # with no Java installed, `alternatives --display java` returns no output

class TestSat5CorrectJava(unittest.TestCase):

    def test_match(self):
        # Match - Satellite 5 with java-1.7.0-ibm
        input_data = {'alternatives_display_java': ALTERNATIVES_IBM_170}
        expected = {'java_alternative': ALTERNATIVE_IBM_170}
        self.assertEqual(expected, sat5_correct_java.main(input_data))

        # Match - Satellite 5 with java-1.8.0-openjdk
        input_data = {'alternatives_display_java': ALTERNATIVES_OPENJDK}
        expected = {'java_alternative': ALTERNATIVE_OPENJDK}
        self.assertEqual(expected, sat5_correct_java.main(input_data))

    def test_error(self):
        # Match - Satellite 5 with no java installed should produce error
        input_data = {'alternatives_display_java': ALTERNATIVES_NONE}
        expected = {'error': 'No java installed or alternatives system missing/missbehaves?'}
        self.assertEqual(expected, sat5_correct_java.main(input_data))

    def test_no_match(self):
        # No match - Satellite 5 with java-1.6.0-ibm
        input_data = {'alternatives_display_java': ALTERNATIVES_IBM_160}
        self.assertEqual(None, sat5_correct_java.main(input_data))
