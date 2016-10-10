#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

L_DEBUG = logging.DEBUG
L_INFO = logging.INFO
L_ERROR = logging.ERROR

logging.basicConfig(level=L_ERROR)
logger = logging.getLogger(__name__)


C_PASS = '\033[92m'
C_WARNING = '\033[93m'
C_FAIL = '\033[91m'
C_ENDC = '\033[0m'
C_BOLD = '\033[1m'
C_UNDERLINE = '\033[4m'

D_TMP = '/tmp'
