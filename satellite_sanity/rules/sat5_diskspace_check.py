#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5', 'Spacewalk']
name = 'There is enough free disk-space in key places'

from satellite_sanity import util


def parse_df_Pk(output):
    """
    Parse df -Pk output with only one line of data like this one:
        [
            'Filesystem                        1024-blocks      Used Available Capacity Mounted on',
            '/dev/mapper/vg_dhcp131222-lv_data   515930552 172570928 317151884      36% /var/satellite'
        ]
    Into list:
        ['/dev/mapper/vg_dhcp131222-lv_data', 515930552, 172570928, 317151884, 36, '/var/satellite']
    """
    assert len(output) == 2
    parsed_raw = output[1].split()
    assert len(parsed_raw) == 6
    parsed = [parsed_raw[0], int(parsed_raw[1]), int(parsed_raw[2]), int(parsed_raw[3]), int(parsed_raw[4][:-1]), parsed_raw[5]]
    return parsed


def parse_df_Pk_or_None(output):
    """
    Uf no df output is provided, return None, else parse it.
    """
    if output:
        return parse_df_Pk(output)
    else:
        return None


def var_lib_pgsql_data(data):
    if not satellite_is_emb_pg(data):
        return None
    version = satellite_version(data)
    if not version:
        return None
    if version.startswith('5.7'):
        return {'desc': 'database', 'required': 1024**2, 'have': parse_df_Pk_or_None(data['df_Pk_opt_rh_postgresql92_root_var_lib_pgsql_data'])}
    else:
        return {'desc': 'database','required': 1024**2, 'have': parse_df_Pk_or_None(data['df_Pk_var_lib_pgsql_data'])}


def var_cache_rhn(data):
    return {'desc': 'cache', 'required': 1024**2, 'have': parse_df_Pk_or_None(data['df_Pk_var_cache_rhn'])}


def var_satellite(data):
    return {'desc': '/var/satellite', 'required': 1024**2, 'have': parse_df_Pk_or_None(data['df_Pk_var_satellite'])}


def satellite_version(data):
    return util.satellite5_version(data['installed-rpms'])


def satellite_is_emb_pg(data):
    return util.satellite5_is_emb_pg(data['rhn_conf'])


def main(data):
    """
    We have various directories with recomended free space. Check that this
    requirement is met.
    """
    volumes = {}
    for this in [var_lib_pgsql_data(data), var_cache_rhn(data), var_satellite(data)]:
        if this is not None:
            vol = this['have'][0]
            if vol not in volumes:
                volumes[vol] = {'size': this['have'][1], 'avail': this['have'][3], 'required': 0, 'what': []}
            volumes[vol]['required'] += this['required']
            volumes[vol]['what'].append(this['desc'])
    volumes_full = {}
    for k, v in volumes.iteritems():
        if v['required'] > v['avail']:
            volumes_full[k] = v
    if len(volumes_full):
        return {'VOLUMES': volumes_full}

def text(result):
    out = ""
    out += "Looks like some of your partitions would use additional space:\n"
    for k, v in result['VOLUMES'].iteritems():
        out += "%s hosts %s and would use %s MB of space\n" % (k, ', '.join(v['what']), (v['required'] - v['avail']) * 1024)
    out += "These limits are not required by documentation and are meant more like a reminder."
    return out
