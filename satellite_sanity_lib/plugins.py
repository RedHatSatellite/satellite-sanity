#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import imp
import glob

from config import logger

from input_data import DataNotAvailable


def load_modules_from_dir(directory):
    """Return list of all modules from given directory"""
    out = []
    mod_path = os.path.join(directory, "[a-z]*.py")
    for name in glob.glob(mod_path):
        # Get name without '.py' extension
        name = os.path.basename(os.path.splitext(name)[0])
        logger.debug("Trying to load rule %s" % name)
        # http://stackoverflow.com/questions/932069/building-a-minimal-plugin-architecture-in-python
        # https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/
        info = imp.find_module(name, [directory])
        mod = imp.load_module(name, *info)
        out.append(mod)
    logger.debug("From '%s' loaded these modules: %s" % (directory, out))
    return out


class Checks(object):
    def __init__(self):
        """Load all checks/modules and store them in self.checks list"""
        self.checks = []
        location = os.path.join(os.path.dirname(__file__), 'checks')
        for mod in load_modules_from_dir(location):
            assert 'tags' in dir(mod), "Check {} missing 'tag' attribute".format([mod])
            assert 'desc' in dir(mod), "Check {} missing 'desc' attribute".format([mod])
            assert 'main' in dir(mod), "Check {} missing 'main' attribute".format([mod])
            self.checks.append(mod)

    def check(self, suggested, data):
        """Return list of tags from 'suggested': first is list of tags that
           passes checks and second is dict of tags whose check(s) did not
           passed (key is tag name and value is why it failed)."""
        passed = set()
        failed = {}
        # Execute all relavant checks and store its results in 'results' dict
        results = {}
        suggested_set = set(suggested)
        relevant_mods = [mod for mod in self.checks if not set(mod.tags).isdisjoint(suggested_set)]
        for mod in relevant_mods:
            result = None
            try:
                results[mod.__name__] = {'out': mod.main(data), 'tags': mod.tags, 'desc': mod.desc}
            except:
                logger.exception('Something failed')
            logger.debug("Check %s returned %s" % (mod.__name__, result))
        # Now take the results of individual checks and compile lists of passed
        # and failed tags
        for result in results.itervalues():
            if result["out"]:
                for tag in result["tags"]:
                    passed.add(tag)
            else:
                for tag in result["tags"]:
                    failed.setdefault(tag, list()).append(result["desc"])

        return passed, failed


class Rules(object):
    result_types = {None: "PASS",
                    False: "SKIP"}

    def __init__(self):
        """Load all rules/modules and store them in self.rules list"""
        self.rules = {}
        location = os.path.join(os.path.dirname(__file__), 'rules')
        for mod in load_modules_from_dir(location):
            assert 'tags' in dir(mod)
            assert 'main' in dir(mod)
            self.rules[mod.__name__] = mod

    def __str__(self):
        """Show stats on which modules we have"""
        out = "We have %s rules loaded:\n" % len(self.rules)
        for mod in self.rules:
            out += "  Rule '%s' can run on %s\n" % (mod.__name__, ', '.join(mod.tags))
        return out

    def list_tags(self):
        """List all tags"""
        results = []
        for item in self.rules.itervalues():
            results.extend(item.tags)
        return list(set(results))

    def list_rules(self, tags):
        """List all rules"""
        results = []
        for mod in self.rules.itervalues():
            # Append this rule only if at least one of its tags belong to tags
            # we should run for
            if not set(tags).isdisjoint(set(mod.tags)):
                r_name = getattr(mod, 'name')
                r_tags = getattr(mod, 'tags')
                results.append({'label': mod.__name__,
                                'name': r_name,
                                'tags': r_tags})
        return results

    def run(self, tags, rules, data):
        """Run rules (run all when "rules" is empty, othervise run only these
           listed there) and return dict with their answers"""
        results = []
        if len(rules) == 0:
          for rule in self.list_rules(tags):
            rules.append(rule["label"])

        for rulename in rules:
            rule = self.rules[rulename]
            try:
                result = rule.main(data)
            except DataNotAvailable:
                logger.error("Data not available for %s" % rule.__name__)
                result = False
            except:
                logger.exception("Something failed badly when executing %s" % rule.__name__)
                result = False

            logger.info("Rule %s returned %s" % (rule.__name__, result))
            # Store list of data rule has used
            used = data.get_access_list()
            # Now if necessary, get description of whats wrong
            if result:
                try:
                    text = rule.text(result)
                    status = "FAIL"
                except:
                    logger.exception("Something failed badly when getting description for %s" % rule["name"])
            else:
                status = Rules.result_types[result]
                text = ""

            results.append({'label': rule.__name__,
                            'status': status,
                            'result': result,
                            'name': rule.name,
                            'text': text,
                            'used': used})
        return results
