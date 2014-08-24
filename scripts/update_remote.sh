#!/bin/bash
#
#  This script gets the zotero database, 
#  and files stored
#
# 

FIREFOX_PROFILE=""

#-----------------------------------------------------------#
# Location of zotero folder must be set by the user

ZOTERO_LOCATION="$HOME/.mozilla/firefox/$FIREFOX_PROFILE/zotero" 
STORAGE_LOCATION=$ZOTERO_LOCATION"/storage"
echo $ZOTERO_LOCATION
echo $STORAGE_LOCATION


ls $STORAGE_LOCATION
mkdir -p  storage

# Copy zotero data to the server
#rsync -avP --delete $STORAGE_LOCATION/  storage
# Copy zotero database
#rsync -avP $ZOTERO_LOCATION/zotero.sqlite  .

# Copy zotero data to the server
sshpass -p "toor1" rsync -avP --delete $HOST:$STORAGE_LOCATION/  storage
# Copy zotero database
sshpass -p "toor1" rsync -avP $HOST:$ZOTERO_LOCATION/zotero.sqlite  .