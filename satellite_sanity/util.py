#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import imp

from config import logger, C_PASS, C_WARNING, C_FAIL, C_ENDC

from input_data import DataNotAvailable

def get_days_uptime(uptime):
  """Return number of days from uptime"""
  # FIXME: what happens when system have uptime in years?
  # Maybe http://bytes.com/topic/python/answers/36189-uptime-unix#td_post_135199
  ###logger.debug("Going to parse %s" % uptime)
  uptime_split = uptime.strip().split(' ')
  if uptime_split[3] == 'days,':
    return int(uptime_split[2])
  elif uptime_split[3] == 'day,':
    return int(uptime_split[2])
  else:
    return 0


def color_pass(text):
  return C_PASS + text + C_ENDC


def color_skip(text):
  return C_WARNING + text + C_ENDC


def color_fail(text):
  return C_FAIL + text + C_ENDC


def load_modules_from_dir(directory):
  """Return list of all modules from given directory"""
  out = []
  for name in os.listdir(directory):
    # Skipp files which are not interested for us
    if not name.endswith(".py") or name == '__init__.py':
      continue
    # Get name without '.py' extension
    name = os.path.splitext(name)[0]
    logger.debug("Trying to load rule %s" % name)
    # http://stackoverflow.com/questions/932069/building-a-minimal-plugin-architecture-in-python
    # https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
    info = imp.find_module(name, [directory])
    mod = imp.load_module(name, *info)
    out.append(mod)
  logger.debug("From '%s' loaded these modules: %s" % (directory, out))
  return out


class checks():
  def __init__(self):
    """Load all checks/modules and store them in self.checks list"""
    self.checks = []
    location = os.path.join(os.path.dirname(__file__), 'checks')
    for mod in load_modules_from_dir(location):
      assert 'tags' in dir(mod)
      assert 'desc' in dir(mod)
      assert 'main' in dir(mod)
      self.checks.append(mod)


  def check(self, suggested, data):
    """Return list of tags from 'suggested': first is list of tags that
       passes checks and second is dict of tags whose check(s) did not
       passed (key is tag name and value is why it failed)."""
    passed = []
    failed = {}
    # Execute all relavant checks and store its results in 'results' dict
    results = {}
    for mod in self.checks:
      # Skipp this check if it is not relevant to any of the requested tags
      # (has no intersection)
      if len([val for val in suggested if val in mod.tags]) == 0:
        continue
      # Finally run the rule
      func = getattr(mod, 'main')
      result = None
      try:
        results[mod.__name__] = {'out': func(data), 'tags': mod.tags, 'desc': mod.desc}
      except:
        logger.exception('Something failed')
      logger.debug("Check %s returned %s" % (mod.__name__, result))
    # Now take the results of individual checks and compile lists of passed
    # and failed tags
    for tag in suggested:
      status = True
      for k, v in results.iteritems():
        if tag in v['tags']:
          if not v['out']:
            status = False
            break
      if status:
        passed.append(tag)
      else:
        if tag in failed:
          failed[tag].append(v['desc'])
        else:
          failed[tag] = [v['desc']]
    return passed, failed


class rules():
  def __init__(self):
    """Load all rules/modules and store them in self.rules list"""
    self.rules = []
    location = os.path.join(os.path.dirname(__file__), 'rules')
    for mod in load_modules_from_dir(location):
      assert 'tags' in dir(mod)
      assert 'main' in dir(mod)
      self.rules.append(mod)


  def __str__(self):
    """Show stats on which modules we have"""
    out = ""
    out += "We have %s rules loaded:\n" % len(self.rules)
    for mod in self.rules:
      out += "  Rule '%s' can run on %s\n" % (mod.__name__, ', '.join(mod.tags))
    return out


  def list_tags(self):
    """List all tags"""
    results = []
    for mod in self.rules:
      for t in getattr(mod, 'tags'):
        if t not in results:
          results.append(t)
    return results


  def list_rules(self, tags):
    """List all rules"""
    results = []
    for mod in self.rules:
      # Skip this rule if there is no intersection of tags we should run
      # and tags this rule should be run for
      if len([val for val in tags if val in mod.tags]) == 0:
        continue
      r_name = getattr(mod, 'name')
      r_tags = getattr(mod, 'tags')
      results.append({'label': mod.__name__, 'name': r_name, 'tags': r_tags})
    return results


  def run(self, tags, data):
    """Run all rules and return dict with their answers"""
    results = []
    for mod in self.rules:
      # Skip this rule if there is no intersection of tags we should run
      # and tags this rule should be run for
      if len([val for val in tags if val in mod.tags]) == 0:
        continue
      # Finally run the rule
      func = getattr(mod, 'main')
      func_text = getattr(mod, 'text')
      name = getattr(mod, 'name')
      result = None
      used = []
      text = ''
      # Reset list of data rule used
      data.reset_access_list()
      # Now run the rule
      try:
        result = func(data)
      except DataNotAvailable:
        logger.error("Data not available for %s" % mod.__name__)
        result = False
      except:
        logger.exception("Something failed badly when executing %s" % mod.__name__)
        result = False
      logger.info("Rule %s returned %s" % (mod.__name__, result))
      # Store list of data rule has used
      used = data.get_access_list()
      # Now if necessary, get description of whats wrong
      if result:
        try:
          text = func_text(result)
        except:
          logger.exception("Something failed badly when getting description for %s" % mod.__name__)
      # Determine what the result was
      if result:
        status = 'FAIL'
      elif result is False:
        status = 'SKIP'
      elif result is None:
        status = 'PASS'
      else:
        logger.error("Failed to understand to result of %s" % result)
        continue
      # Save what was returned
      results.append({'label': mod.__name__, 'status': status, 'result': result, 'name': name, 'text': text, 'used': used})
    return results
