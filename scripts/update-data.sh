#!/usr/bin/env bash
#
#  This script gets the zotero database, 
#  and files stored
#
#----------------------------------#
#   U S E R   S E T T I N G S      #
#----------------------------------#

FIREFOX_PROFILE="mwad0hks.default"
ZOTSERVER_DATA=$HOME/.zotserver         # Destination Directory

#----------------------------------#
#   AUTOMATED SECTION              #
#----------------------------------#
#
# Don't edit this section unless it is necessary.
#
ZOTERO_LOCATION="$HOME/.mozilla/firefox/$FIREFOX_PROFILE/zotero"

mkdir -p $ZOTSERVER_DATA


STORAGE_LOCATION=$ZOTERO_LOCATION/storage
echo $ZOTERO_LOCATION
echo $STORAGE_LOCATION

#ls $STORAGE_LOCATION
mkdir -p  storage
# Copy zotero data to the server
rsync -avP --delete $STORAGE_LOCATION/ $ZOTSERVER_DATA/storage
# Copy zotero database
rsync -avP $ZOTERO_LOCATION/zotero.sqlite  $ZOTSERVER_DATA





