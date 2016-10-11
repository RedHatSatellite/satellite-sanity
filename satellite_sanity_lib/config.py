#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.handlers

APP = 'satellite-sanity'

L_DEBUG = logging.DEBUG
L_INFO = logging.INFO
L_ERROR = logging.ERROR

# From https://docs.python.org/2/howto/logging-cookbook.html#multiple-handlers-and-formatters
logger = logging.getLogger(APP)
logger.setLevel(level=logging.DEBUG)
# Create console handler wich logs only info messages and above by default
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
ch.setFormatter(formatter)
# Create file handler which logs even debug messages
fh = logging.handlers.RotatingFileHandler('/tmp/%s.log' % APP, maxBytes=1024*1024, backupCount=1)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
# Add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

C_PASS = '\033[92m'
C_WARNING = '\033[93m'
C_FAIL = '\033[91m'
C_ENDC = '\033[0m'
C_BOLD = '\033[1m'
C_UNDERLINE = '\033[4m'

D_TMP = '/tmp'
