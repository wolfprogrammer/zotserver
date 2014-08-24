#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Library to Parse configuration file
"""
import sys
import re





def ParseConfFile(filename, separator="=", comment_symbol="#"):
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

    text = open(filename).read()

    entry_pattern = re.compile("(.*)%s(.*)" % separator)
    line_comment_pattern = re.compile("%s.*" % comment_symbol, re.M)

    _text= line_comment_pattern.sub("" , text)
    _test = _text

    data = entry_pattern.findall(_text)
    data = [(k.strip(), v.strip()) for k,v in data]
    return dict(data)


print ParseConfFile("zotserver.conf")





