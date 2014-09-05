#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to extract data from Zotero database

This module allows to export and extract Zotero's
data to external applications.

@TODO: Add a better module docstring
@TODO: Make database (Sqlite) thread safe
@TODO: Create an object to handle the database and close it each request

"""
# from __future__ import unicode_literals
import sqlite3
import os.path
from PyLib import Config

import logging
import logging.config
from PyLib import LOG_SETTINGS
logger = logging.getLogger("lib")


class Zotero():
    """
    Open zotero database and query the data.

    """

    def __init__(self, database, storage, zotdir):
        """
        :param database:  Datbase file
        :param storage:   Storage directory
        :return:
        :type database:   str
        :type storage:    str
        :rtype : None
        """
        self.database = os.path.join(zotdir, database)
        self.storage = os.path.join(zotdir, storage)
        self.zotdir  = zotdir

        logger.warn("Opening database database=%s database=%s" % (database, storage))


    def open_database(self):
        """
        :return: conn, cur
        First function of this module that needs to be executed
        open a connection to zotero database

        """
        # Connect to database file
        logger.debug("Opening database = %s" % self.database)
        conn = sqlite3.connect(self.database, timeout=10)
        cur = conn.cursor()
        return conn, cur


    def close_database(self, conn):
        conn.close()
        return 0

    def create_text_index(self):
        """
        Creates the table: fulltxt, using the module FTS3
        to allow full text search in the database

        """

        #  Create Virtual table fulltxt( wordID, Word, itemID
        sql1 = """
        CREATE VIRTUAL TABLE IF NOT EXISTS fulltxt USING FTS3
        (
        wordID   INTEGER,
        word     TEXT,
        itemID   INTEGER
        )
        ;
        """

        # Populate virtual table
        sql2 = """
        INSERT     INTO fulltxt
        SELECT     fulltextWords.wordID, fulltextWords.word , fulltextItemWords.itemID
        FROM       fulltextWords , fulltextItemWords
        WHERE      fulltextWords.wordID = fulltextItemWords.wordID
        ;
        """
        conn, cur = self.open_database()

        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
        conn.close()

    def text_search(self, text):

        sql = """

        SELECT   itemID FROM fulltxt
        WHERE  word MATCH ?
        GROUP BY itemID

        """
        conn, cur = self.open_database()

        itemids = []


        query = cur.execute(sql, (text,))
        rows = query.fetchall()

        #    print rows

        for row in rows:
            itemid = row[0]
            itemids = itemids + [itemid]

        conn.close()
        return itemids


    def create_itemName_view(self):
        """
        Create viw:  item_names

        """

        sql = """
            CREATE VIEW item_names AS

            SELECT DISTINCT itemData.itemID,  itemDataValues.value
            FROM      itemData, itemDataValues  , fields
            WHERE     itemData.valueID =  itemDataValues.valueID AND
                      fields.fieldID = itemData.fieldID AND itemData.fieldID=110
            ORDER BY  itemID

        """
        conn, cur = self.open_database()
        cur.execute(sql)
        conn.commit()

    #create_itemName_view();

    def get_tags(self):
        """
        Get all zotero tags

        @type  void
        @param void:  Command that will be executed and returned output
        @rtype     :  List
        @returns  :  [ tagID , tags ]


        """
        sql_query_tags = """
        SELECT tagID, name  FROM  tags ;
        """
        conn, cur = self.open_database()
        query = cur.execute(sql_query_tags)
        rows = query.fetchall()
        conn.close()

        return rows

    def get_tagname(self, tagid):

        sql = """
        SELECT name
        FROM  tags
        WHERE tagid = ?
        ;
        """
        conn, cur = self.open_database()

        query = cur.execute(sql, (tagid,))
        rows = query.fetchall()

        if rows != []:
            rows = rows[0]
            rows = rows[0]
            return rows
        conn.close()
        return []

    def get_related_tags(self, tagid):
        """
        Gets all tags related to tagid
        :param tagid: Tag be searched
        :type tagid: int
        :return: List of tuples [(id0, "tag1", (id1, "tag1)" ...]
        :rtype:  lst
        """
        sql = """
        SELECT DISTINCT B.tagID, C.name
                  FROM (SELECT * FROM itemTags WHERE tagID = ?) as A,
                  itemTags as B,
                  tags as C
        WHERE A.itemID = B.itemID and B.tagID = C.tagID
        ORDER BY C.name
        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (tagid,))
        rows = query.fetchall()
        conn.close()

        # if rows:
        #     rows = [r[0] for r in rows]

        return rows


    def get_collection_name(self, collid):

        sql = """
        SELECT collectionName
        FROM  collections
        WHERE collectionID = ?
        ;
        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (collid,))
        rows = query.fetchall()

        if rows != []:
            rows = rows[0]
            rows = rows[0]
            return rows
        conn.close()
        return []

    def get_collections(self):
        """
        Get all collections and return in a list

        """

        sql = """
        SELECT  collectionID, collectionName  FROM collections ;
        """
        conn, cur = self.open_database()
        query = cur.execute(sql)
        rows = query.fetchall()
        conn.close()
        return rows

    def get_collections_items(self):
        """
        Get all items from all collections.

        Returns [ collectionDI, collectionName, colllectionItem ]

        """

        sql = """
        SELECT collections.collectionID,  collections.collectionName,  collectionItems.itemID
        FROM collections, collectionItems
        WHERE  collections.collectionID =  collectionItems.collectionID    ;
        """
        conn, cur = self.open_database()
        query = cur.execute(sql)
        rows = query.fetchall()
        conn.close()
        return rows

    def get_item_from_collections(self, collid):
        """
        Return list of all itemID from some collection,
        given the collectionID

        """

        sql = """
        SELECT  collectionItems.itemID
        FROM collections, collectionItems
        WHERE      collections.collectionID =  collectionItems.collectionID
               AND collectionItems.collectionID = ? ;
        """
        conn, cur = self.open_database()

        query = cur.execute(sql, (collid,))
        rows = query.fetchall()

        itemids = []

        for row in rows:
            itemid = row[0]
            itemids = itemids + [itemid]

        conn.close()

        return itemids

    def get_subcollections(self, collid):
        """
        Returns the subcollection IDs of a collection

        collid: Collection ID

        Returns a list of ( collectionID, CollectionName )

        [ ( collid1, coll1_name ) ,  ( collid2, coll2name ), .... ]

        """


        sql = """
            SELECT 	collectionID, collectionName
            FROM    collections
            WHERE 	parentCollectionID = ?
        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (collid,))
        rows = query.fetchall()

        conn.close()
        logger.debug("rows = %s" % rows)
        return rows

    def get_collections_parents(self):
        sql = """
        SELECT collectionID, CollectionName
        FROM    collections
        WHERE parentCollectionID IS NULL ;
        """
        conn, cur = self.open_database()

        query = cur.execute(sql)
        rows = query.fetchall()
        conn.close()
        return rows

    def list_tags(self):
        """
        #print all zotero tags

        @type  void
        @param void
        @rtype void

        """
        rows = self.get_tags()

        for row in rows:
            tagID, tag = row
            print str(tagID) + "\t" + tag

    def list_collections(self):
        """
        print all Zotero collections

        """

        rows = self.get_collections()

        for row in rows:
            collID, collection = row
            #print str(collID) + "\t" + collection

    def get_item_ids(self):
        """
        Return the itemID of all items
        """

        sql = """
        SELECT itemID FROM items
        ORDER BY itemID
        ;
        """
        conn, cur = self.open_database()
        itemids = []

        query = cur.execute(sql)
        rows = query.fetchall()

        #    print rows

        for row in rows:
            itemid = row[0]
            itemids = itemids + [itemid]

        conn.close()
        return itemids

    def get_items(self):
        """
        Get all items in zotero library

        """

        sql = """
        SELECT DISTINCT itemData.itemID,  itemDataValues.value
        FROM      itemData, itemDataValues  , fields
        WHERE     itemData.valueID =  itemDataValues.valueID AND
                  fields.fieldID = itemData.fieldID AND itemData.fieldID=110
        ORDER BY  itemID
        ;
        """

        conn, cur = self.open_database()
        query = cur.execute(sql)
        rows = query.fetchall()
        conn.close()
        return rows

    def list_items(self):
        """
        Print all items in zotero library.
        """

        rows = self.get_items()

        for row in rows:
            itemID, itemName = row
            print str(itemID) + "\t" + itemName

    def filter_tag(self, tagid):
        """
           Filter item by tags
           """

        sql = """
           SELECT itemTags.itemID
           FROM itemTags
           WHERE itemTags.tagID = ?
           ;

           """
        conn, cur = self.open_database()

        query = cur.execute(sql, (tagid,))
        rows = query.fetchall()

        itemids = []

        for row in rows:
            itemid = row[0]
            itemids = itemids + [itemid]

        conn.close()
        return itemids

    def get_item_tags(self, itemid):
        """
        :param itemid:
        :type itemid: int
        :return:
        :rtype:  lst
        """

        sql = """
        SELECT A.tagID, B.name  FROM
            (SELECT itemTags.tagID FROM itemTags WHERE    itemTags.itemID =  ? ) as A,
            tags as B
        WHERE A.tagID = B.tagID
        """

        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid,))
        rows = query.fetchall()
        conn.close()
        return rows




    def get_item_data(self, itemid):

        sql = """

        SELECT  fields.fieldName , itemDataValues.value

        FROM      itemData, itemDataValues  , fields

        WHERE   itemData.valueID =  itemDataValues.valueID AND
            fields.fieldID = itemData.fieldID  	   AND
            itemData.itemID = ?

        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid,))
        rows = query.fetchall()
        conn.close()

        return rows

    def list_item_data(self, itemid):

        rows = self.get_item_data(itemid)

        for row in rows:
            data_type, value = row
            print data_type + "\t\t" + value + "\n"

    def get_item_attachment(self, itemid):
        sql = """
        SELECT    items.key, itemAttachments.path
        FROM      items,     itemAttachments
        WHERE   items.itemID = itemAttachments.itemID AND items.itemID = ?
        ORDER BY items.itemID
        ;
        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid,))
        row = query.fetchall()
        conn.close()

        #print row

        if len(row) != 0:
            dirr, name = row[0]

            #print type(dirr)
            #print type (name)

            if name is not None:
                name = name.split("storage:")[1]

                #print "trace 1"
            else:
                #print "trace2"
                return -1

            if dirr is not None:
                #print "trace 3"
                #ffile = STORAGE_PATH + dirr + "/" + name
                ffile = os.path.join(self.storage, dirr, name)
                print ffile
            else:
                return -1

            return ffile

    def get_attachment2(self, itemid):

        sql = """
        SELECT * FROM (
        SELECT items.itemID,  items.key, itemAttachments.path,  itemAttachments.mimeType, itemDataValues.value
        FROM items
        LEFT JOIN itemAttachments
        ON itemAttachments.itemID = items.itemID
        LEFT JOIN itemData
        ON  itemData.itemID = items.itemID  AND itemData.fieldID=110
        LEFT JOIN itemDataValues
        ON itemDataValues.valueID = itemData.valueID
        ORDER BY items.itemID
        )
        WHERE itemID > 1 AND itemID = ? ;

        """
        logger.debug("Query attachment2 itemid = %s " % itemid)
        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid,))
        rows = query.fetchall()
        conn.close()

        if rows == []:
            return None

        data, key, path, mtype, title = rows

        logger.debug({"data": data, "path": path, "mtype": mtype, "title": title})

        if title is None:
            return None

        if path is None:
            data2 = self.get_attachment(itemid + 1);
            return data2

        fname = path.split("storage:")[1]
        PATH = os.path.join(self.storage, key, fname)

        return PATH

    def get_attachment(self, itemid):
        logger.debug("Get attachment itemid = %s " % itemid)

        sql = """
        SELECT  path,  key FROM
        (
        SELECT  itemAttachments.itemID, itemAttachments.sourceItemID, itemAttachments.path , items.key
        FROM itemAttachments, items
        WHERE  itemAttachments.itemID  = items.itemID
        )
        WHERE itemID= ?  OR sourceItemID = ? ;

        """
        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid, itemid))
        rows = query.fetchall()
        conn.close()

        if rows == []:
            return None
        else:
            path, key = rows[0]

            logger.debug({"itemid": itemid, "path": path, "key": key})

            if path == None:
                if len(rows) == 1:
                    return None
                path, key = rows[1]
            # IndexError('list index out of range',)
            try:
                fname = path.split("storage:")[1]
            except:
                fname = ""


            PATH = os.path.join(self.storage, key, fname)
            return PATH


def main():

    zotero = Zotero(Config.DATABASE, Config.STORAGE, Config.ZOTDIR)

    print zotero.list_items()
    print 10*"-"

    print zotero.get_item_tags(116)
    print 10*"-"

    print zotero.get_related_tags(1)
    print 10*"-"

if __name__ == "__main__":
    main()


