#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Library to Parse configuration file
"""


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

    _text= line_comment_pattern.sub("" , text)
    _test = _text

    data = entry_pattern.findall(_text)
    #data = [(k.strip(), v.strip()) for k,v in data]
    Config = Container()

    for k, v in data:
        Config.set(k.strip(), v.strip())

    #return dict(data)
    return Config

Config = parse_confFile("zotserver.conf")

#c = Container()
#c.copy(Config1)

def test():
    print Config
    print Config.HOST
    print Config.LOGFILE
    print Config.STORAGE
    print Config.DATABASE
    print Config.PORT

#test_config()

