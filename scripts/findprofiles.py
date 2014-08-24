#!/usr/bin/env python2
#
#   Find Zotero storage directory
#
#   Usage
#
#
#
#------------------------------------------------

import os
import sys
import platform

HOME = os.path.expanduser("~")
USERNAME = os.path.basename(HOME)

#  C:\Documents and Settings\<username>\Application Data\Mozilla\Firefox\Profiles<randomstring>\zotero 

if    sys.platform.startswith('linux') or sys.platform.startswith('darwin') or sys.platform.startswith('bsd'):
    FIREFOX = os.path.join(HOME, ".mozilla/firefox")

elif sys.platform.startswith('win32'):   
    FIREFOX = "C:\Users\%s\Appdata\Mozilla\Firefox" % USERNAME


def find_firefox_profiles():
    
    profiles = []
    
    for directory in os.listdir(FIREFOX):
        path = os.path.join(FIREFOX, directory) 
        if os.path.isdir(path):
            profiles.append(directory)
    try:
        profiles.remove("Crash Reports")
    except:
        pass
    return profiles
    
#profiles = find_firefox_profiles()  
#print profiles


def find_zotero_directory():
    
    profiles = find_firefox_profiles()  
    zotero = {}

    for profile in profiles:
        zotdir = os.path.join(FIREFOX, profile, "zotero")
        if os.path.isdir(zotdir):
            zotero[profile] = zotdir
            
    return zotero

print "USERNAME = ", USERNAME
print "FIREFOX  = ", FIREFOX
print find_zotero_directory()
