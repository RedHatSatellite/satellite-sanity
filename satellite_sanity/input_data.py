#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import subprocess
import ConfigParser
import tempfile
import datetime

from config import logger

class DataNotAvailable(Exception):
    pass

class InputData():
  def __init__(self, data_dir=None):
    self.__data = {}   # data storage (e.g. key/label = 'hostname-s'
                       # and value = 'dhcp123-45')
    self.__data_dir = data_dir   # if set to none, when asked for some label,
                                 # execute coresponding command, if set to
                                 # string, it is a directory and when asked
                                 # for label return content of coresponding
                                 # file
    self.__access_list = {}
    self.__config_filename = os.path.join(os.path.dirname(__file__), 'config.ini')
    self.__config_commands_section = 'commands'
    self.__config_files_section = 'files'
    self.__load_config()

  def __load_config(self):
    """Loads mapping of label to actual command in case we are running on live
       system and label to possible files in case we are running from dump."""
    config = ConfigParser.SafeConfigParser()
    config.optionxform = str
    config.read(self.__config_filename)
    self.config = {}
    self.config['commands'] = dict(config.items(self.__config_commands_section))
    self.config['files'] = {}
    for k, v in dict(config.items(self.__config_files_section)).iteritems():
      self.config['files'][k] = v.splitlines()
    logger.debug("Loaded commands and files config %s" % self.config)

  def __load(self, label):
    """Get output of coresponding command or if __data_dir is set load
       content of coresponding file and store it to self.__data[label].
       If command fails, usually "['']" is stored."""
    assert label not in self.__data
    # Are we running on live system or from directory?
    if self.__data_dir == None:
      if label not in self.__access_list:
        self.__access_list[label] = self.config['commands'][label]
      # TODO: Add some timeouts, ulimit, nice... (?)
      logger.debug("Going to execute '%s' for '%s'" % (self.config['commands'][label], label))
      # FIXME: is it OK to have shell=True here from secuity stand-point?
      process = subprocess.Popen([self.config['commands'][label]], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # FIXME: is this correct way to run this? Can not we got stuck when the data are too big?
      stdout, stderr = process.communicate()
      if len(stderr) != 0:
        logger.warn("Command '%s' failed with '%s'" % (self.config['commands'][label], stderr))
        raise DataNotAvailable("Command '%s' failed with '%s'" % (self.config['commands'][label], stderr))
      self.__data[label] = stdout.strip().split("\n")
    else:
      our_file = None
      our_file_rel = None
      for relative_file in self.config['files'][label]:
        f = os.path.join(self.__data_dir, relative_file)
        if os.path.isfile(f):
          our_file = f
          our_file_rel = relative_file
          break
      if our_file:
        logger.debug("Going to load '%s' for '%s'" % (f, label))
        if label not in self.__access_list:
          self.__access_list[label] = our_file_rel
        try:
          fp = open(f, 'r')
        except IOError:
          logger.warn("Failed to load %s for %s" % (f, label))
          raise DataNotAvailable("Failed to load %s for %s" % (f, label))
        self.__data[label] = fp.read().splitlines()
        fp.close()
      else:
        logger.warn("Suitable file for %s not found" % label)
        raise DataNotAvailable("Suitable file for %s not found" % label)

  def __getitem__(self, label):
    if label not in self.__data:
      self.__load(label)
    return self.__data[label]

  def __setitem__(self, label, data):
    self.__data[label] = data

  def __str__(self):
    return "Input data (loaded: %s, configured: %s, data_dir: %s)" % (self.__data.keys(), self.config['commands'].keys(), self.__data_dir)

  def save(self):
    """Dump all data we can collect to tmp directory"""
    data_dir_timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    data_dir_prefix = 'satellite-sanity-save-%s' % data_dir_timestamp
    data_dir = tempfile.mkdtemp(suffix='', prefix=data_dir_prefix)
    logger.debug("Saving to directory %s" % data_dir)
    for key in self.config['commands'].keys():
      data_file = os.path.join(data_dir, key)
      fd = open(data_file, 'w')
      try:
        for row in self[key]:
          fd.write("%s\n" % row)
      except AssertionError:
        logger.warn("Failed when obtaining %s" % key)
      fd.close()
      data_file_lines = len(self[key]) if self[key] is not None else -1,
      logger.debug("Saved %s lines to %s" % (data_file_lines, data_file))
    return data_dir

  def get_access_list(self):
    """Return list of labes requested so far"""
    return self.__access_list

  def reset_access_list(self):
    """Clear list of labes requested so far"""
    self.__access_list = {}
