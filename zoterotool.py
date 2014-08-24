#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to extract data from Zotero database

This module allows to export and extract Zotero's
data to external applications.

TODO: Add a better module docstring
TODO: Make database (Sqlite) thread safe
TODO: Create an object to handle the database and close it each request

"""
# from __future__ import unicode_literals
import sqlite3
import os.path
from Config import Config
from Logger import logger



class Zotero():
    """

    """

    def __init__(self, database, storage):
        """
        :param database:  Datbase file
        :param storage:   Storage directory
        :return:
        :type database:   str
        :type storage:    str
        :rtype : None
        """
        self.database = database
        self.storage = storage

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
                ffile = os.path.join(STORAGE_PATH, dirr, name)
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
        conn, cur = self.open_database()
        query = cur.execute(sql, (itemid,))
        rows = query.fetchall()
        conn.close()

        ##print rows

        if rows == []:
            return None

        data = rows[0]

        key = data[1]

        path = data[2]

        mtype = data[3]

        title = data[4]

        #if name is None:

        #    #print "tr1"
        #    return None

        if title is None:
            return None

        if path is None:
            #        #print "tr2"

            data2 = self.get_attachment(itemid + 1);
            #        #print "data2 ="
            #        #print data2
            return data2

        ##print "tr3"

        fname = path.split("storage:")[1]
        PATH = os.path.join(STORAGE_PATH, key, fname)
        ##print PATH


        return PATH

    def get_attachment(self, itemid):

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

        #print "item= " + str(itemid)
        #print rows


        if rows == []:
            return None
        else:

            #print "------------"
            path, key = rows[0]
            #print itemid
            #print "path = " + path
            #print "key = "  + key



            if path == None:
                if len(rows) == 1:
                    return None

                path, key = rows[1]

            fname = path.split("storage:")[1]

            PATH = os.path.join(STORAGE_PATH, key, fname)

            return PATH


    #    return rows


    # Close database connection
    #conn.close()

    # if __name__ == "__main__":
    #     #print "Testing"
    #
    #     open_database(DATABASE2);
    #     #list_items();



def main():

    zotero = Zotero(Config.DATABASE, Config.STORAGE)

    print zotero.list_items()

if __name__ == "__main__":
    main()


