#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project configuration library. This library can
be resused in almost any project.

It provides logging, configuration parser and resourse file.

"""

import logging
import logging.config
import os
import shutil

HOME = os.path.expanduser("~")


def this():
    """
    Returns the absolute path to the script that calls this function
    """
    import os
    import inspect
    return os.path.abspath(inspect.stack()[1][1])

def this_dir():
    """
    Returns the absolute path to script directory that calls this function
    """
    import os
    import inspect
    return os.path.dirname(os.path.abspath(inspect.stack()[1][1]))

def get_resource_path(filename):
    """
    :param filename: (str)  Name of file in same directory of script
    Returns absolute path to file in same directory that this function
    is being called.
    """

    import os
    import inspect
    return os.path.join( os.path.dirname(os.path.abspath(inspect.stack()[1][1])), filename)

def get_resource_file(filen):
    """
    :param filen: (str) File name of resource file
    :return:

    Return content of file in same directory of the script calling
    this routine or inside the zip file if the script is imported
    from a zip file ( Python egg file).

    """
    import zipfile
    import os
    import inspect
    this_directory = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    #logger.debug("Getting resource file %s" % filen)

    if zipfile.is_zipfile(this_directory):
       #logger.debug("ZIP FILE")
       zf = zipfile.ZipFile(this_directory)
       data = zf.read(filen)

    else:
       #logger.debug("NOT ZIP FILE")
       data = open(os.path.join(this_directory, filen)).read()

    return data

def mkdir(path):
    import os
    if not os.path.isdir(path):
        os.mkdir(path)


class Container(dict):

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def set(self, key, value):
        self[key] = value
#        self.__keys__.append(key)

    def get(self, key):
        return self[key]


    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

def parse_confFile(filename, separator="=", comment_symbol="#"):
    """
    :param filename:        Filename to be parsed
    :param separator:       Separtor between entry
    :param comment_symbol:  Comment symbol
    :return:                Dictionary containing the entries and values in config file.
    :type  filename:        str
    :type  separator:       str
    :type  comment_symbol:  str
    :type return: dict

    Parse a configuration file like:

            # Storage directory
            STORAGE  = ./storage
            DATABASE = zotero.sqlite
            PORT = 8080
            HOST = 0.0.0.0
            LOGFILE = /tmp/zotero.log

    and returns:

    {'LOGFILE ': ' /tmp/zotero.log', 'STORAGE  ': ' ./storage', 'DATABASE ...}


    """
    import re
    text = open(filename).read()

    entry_pattern = re.compile("(.*)%s(.*)" % separator)
    line_comment_pattern = re.compile("%s.*" % comment_symbol, re.M)

    _text= line_comment_pattern.sub("", text)
    _test = _text

    data = entry_pattern.findall(_text)
    #data = [(k.strip(), v.strip()) for k,v in data]
    Config = Container()

    for k, v in data:
        Config.set(k.strip(), v.strip())

    #return dict(data)
    return Config

zotserverconf = os.path.join(HOME, ".zotserver.conf")


if not os.path.exists(zotserverconf):
    print "Creating configuration file %s" % zotserverconf
    try:
        print "copying user file"
        shutil.copyfile(get_resource_path("templates/zotserver.conf"), zotserverconf)
    except:
        pass

Config = parse_confFile(zotserverconf)

for dirp in ['log', 'storage' ]:
    mkdir(os.path.join(Config.ZOTDIR, dirp))

debug_log = os.path.join(Config.ZOTDIR, 'log', 'debug.log')
request_log = os.path.join(Config.ZOTDIR, 'log', 'request.log')


LOG_SETTINGS = {
    # --------- GENERAL OPTIONS ---------#
    'version': 1,
    'disable_existing_loggers': False,

    # ---------- LOGGERS ---------------#

    'loggers':{
        'root': {
            'level': 'NOTSET',
            'handlers': ['console', 'file'],
        },
        'lib': {
            'level': 'NOTSET',
            'handlers': ['file'],
        },
        'request': {
            'level': 'INFO',
            'handlers': ['console', 'file2'],
        },
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
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'NOTSET',
                'formatter': 'detailed',
                'filename': debug_log,
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
        },
        'file2': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'NOTSET',
                'formatter': 'request',
                'filename': request_log,
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
        },
        'null':{
            'class': 'logging.NullHandler'
        },
    },
    # ----- FORMATTERS -----------------#
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(funcName)s() ' \
                      '%(levelname)-8s %(message)s\n',
        },
        'request': {
            'format': 'REQUEST %(asctime)s   %(message)s\n',
        },
    },
}

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger("root")
request_logger = logging.getLogger("request")