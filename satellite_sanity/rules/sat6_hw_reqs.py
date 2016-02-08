#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_6', 'Satellite_6_preinst']
name = 'Check basic HW requirements'

from satellite_sanity import util


def cpu_cores(data):
  """
  Return number of cores so we can check we have >= 2 on x86_64.
  """
  return util.cpu_cores(data['proc_cpuinfo'])


def ram_size(data):
  """
  Return RAM size so we can ensure wa have >=12GB of it.
  """
  return util.ram_size(data['proc_meminfo'])


def swap_size(data):
  """
  Return swap size in B so we can ensure wa have >=4GB of it.
  """
  return util.swap_size(data['proc_meminfo'])


def main(data):
  out = []
  var_cpu_cores = cpu_cores(data)
  exp_cpu_cores = 2
  var_ram_size = ram_size(data)
  exp_ram_size = 1024 * 1024 * 12
  var_swap_size = swap_size(data)
  exp_swap_size = 1024 * 1024 * 4
  if var_cpu_cores < exp_cpu_cores:
    out.append("%s CPU cores is below minimal requirement of %s" % (var_cpu_cores, exp_cpu_cores))
  if var_ram_size < exp_ram_size:
    out.append("RAM size %s kB is below minimal requirement of %s kB" % (int(round(var_ram_size)), exp_ram_size))
  if var_swap_size < exp_swap_size:
    out.append("Swap size %s kB is below minimal requirement of %s kB" % (int(round(var_swap_size)), exp_swap_size))
  if out:
    return {'errors': out}


def text(result):
  out = ""
  out += "System running Satellite 6 should meet minimal required HW configuration:\n"
  for e in result['errors']:
    out += "  %s\n" % e
  out += "See https://access.redhat.com/documentation/en-US/Red_Hat_Satellite/6.1/html/Installation_Guide/sect-Red_Hat_Satellite-Installation_Guide-Prerequisites.html#sect-Red_Hat_Satellite-Installation_Guide-Prerequisites-Base_Operating_System"
  return out
