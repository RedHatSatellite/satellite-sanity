#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5']
name = 'Database have correct encoding set'

def satellite_db_backend(data):
    for line in data['rhn_conf']:
        if line.startswith('db_backend'):
            backend = line.split('=')[1].strip()
            assert backend in ('postgresql', 'oracle')
            return backend

def main(data):
    if data['rhn_charsets']:
        db_backend = satellite_db_backend(data)
        db_first = ''
        db_second = ''
        # Load server and client encoding
        if db_backend == 'postgresql':
            server_encoding = ''
            server_encoding_close = None
            client_encoding = ''
            client_encoding_close = None
            for line in data['rhn_charsets']:
                if server_encoding_close:
                    server_encoding_close -= 1
                    if server_encoding_close == 0:
                        server_encoding = line.strip()
                if client_encoding_close:
                    client_encoding_close -= 1
                    if client_encoding_close == 0:
                        client_encoding = line.strip()
                if line.strip() == 'server_encoding':
                    server_encoding_close = 2
                    continue
                if line.strip() == 'client_encoding':
                    client_encoding_close = 2
                    continue
            db_first = server_encoding
            db_second = client_encoding
        if db_backend == 'oracle':
            NLS_CHARACTERSET = ''
            NLS_NCHAR_CHARACTERSET = ''
            for line in data['rhn_charsets']:
                if line.startswith('NLS_CHARACTERSET'):
                    NLS_CHARACTERSET = line.split()[1]
                if line.startswith('NLS_NCHAR_CHARACTERSET'):
                    NLS_NCHAR_CHARACTERSET = line.split()[1]
            db_first = NLS_CHARACTERSET
            db_second = NLS_NCHAR_CHARACTERSET
        # Evaluate if what we have loaded is correct
        if db_first != '' and db_second != '':
            if db_first != 'UTF8' or db_second != 'UTF8':
                return {'db_first': db_first, 'db_second': db_second}

def text(result):
    out = ""
    out += "Your DB do not have correct encoding set (%s and %s)\n" % result.values()
    out += "See https://access.redhat.com/solutions/711063"
    return out
