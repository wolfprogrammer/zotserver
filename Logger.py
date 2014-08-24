#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
from Config import Config

LOG_SETTINGS = {
    # --------- GENERAL OPTIONS ---------#
    'version': 1,
    'disable_existing_loggers': False,

    # ---------- LOGGERS ---------------#
    'root': {
        'level': 'NOTSET',
        'handlers': ['file', 'console'],
    },

    # ---------- HANDLERS ---------------#
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },

        'file': {
            'class': 'logging.FileHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'filename': Config.LOG,
            'mode': 'w',
        },

    },

    # ----- FORMATTERS -----------------#
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(funcName)s() ' \
                      '%(levelname)-8s %(message)s',
        },
    },
}

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger("root")
