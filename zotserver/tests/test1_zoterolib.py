#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
this = os.path.abspath(__file__)
this_dir = os.path.dirname(this)
sys.path.append(os.path.join(this_dir, '..'))


from zoterolib import Zotero
from PyLib import Config

zotero = Zotero(Config.DATABASE, Config.STORAGE, Config.ZOTDIR)

# Fetch collection ID data
collection_id = 30

collname = zotero.get_collection_name(collection_id)
print "collname = ", collname


itemsIDs = zotero.get_item_from_collections(collection_id)

print "items = ", itemsIDs

for itemid in itemsIDs:

    filepath = zotero.get_attachment(itemid)

    print "itemid ", itemid
    print "path   ", filepath
    print ""

