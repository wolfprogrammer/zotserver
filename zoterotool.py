#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to extract data from Zotero database

This module allows to export and extract Zotero's
data to external applications.



"""
#from __future__ import unicode_literals    

import sqlite3 as sq
import os.path
from  os.path import isfile  
from  os import system


# Location of zotero folder must be set by the user
ZOTERO_LOCATION =  ".mozilla/firefox/i1thdo2f.Capes/zotero/"


global HOME
global STORAGE_PATH
# Paths
#HOME = os.path.expanduser("~/")
#PATH= HOME + "zotero-server/"
STORAGE_PATH= "storage/"

#print PATH

#  Create a copy of zotero database due to lock issues.
#
#DATABASE2 = PATH + "zotero.sqlite"
DATABASE2 =  "zotero.sqlite"

#system("cp " + DATABASE1 + " " +  DATABASE2 )

global conn
global cur


def open_database(database):
    """
    First function of this module that needs to be executed
    open a connection to zotero database

    """
    global conn
    global cur

    
    # Connect to database file
    conn= sq.connect(database,timeout=10)
    cur = conn.cursor()



def close_database():
    conn.close()
    return 0




def create_text_index():
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
    
    cur.execute(sql1)   
    cur.execute(sql2)
    conn.commit()



def text_search(text):

    sql = """

    SELECT   itemID FROM fulltxt 
    WHERE  word MATCH ?
    GROUP BY itemID

    """

    
    itemids = [ ]

    query=cur.execute(sql,(text,))   
    rows =query.fetchall()

#    print rows

    for row in rows:
        itemid = row[0]
        itemids = itemids + [itemid]

    return itemids           



def create_itemName_view(): 
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
    query=cur.execute(sql)   
    conn.commit()




#create_itemName_view();


def  get_tags():
    """
    Get all zotero tags

    @type  void
    @param void:  Command that will be executed and returned output
    @rtype     :  List 
    @returns  :  [ tagID , tags ]


    """

    sql_query_tags= """
    SELECT tagID, name  FROM  tags ; 
    """

    query=cur.execute(sql_query_tags )  
    rows=query.fetchall()


    ##print rows
    return rows



def get_tagname(tagid):
    
    sql= """
    SELECT name  
    FROM  tags
    WHERE tagid = ?    
    ; 
    """

    query=cur.execute(sql,(tagid,))  
    rows=query.fetchall()

    if rows != []:
        rows = rows[0]
        rows = rows[0]
        return rows 

    return []

def get_collection_name(collid):
    
    sql= """
    SELECT collectionName  
    FROM  collections
    WHERE collectionID = ?    
    ; 
    """

    query=cur.execute(sql,(collid,))  
    rows=query.fetchall()

    if rows != []:
        rows = rows[0]
        rows = rows[0]
        return rows 

    return []
                     

def get_collections():
    """
    Get all collections and return in a list

    """

    sql="""
    SELECT  collectionID, collectionName  FROM collections ;
    """ 
    query=cur.execute(sql)  
    rows=query.fetchall()

    return rows


def get_collections_items():
    """
    Get all items from all collections.

    Returns [ collectionDI, collectionName, colllectionItem ]

    """

    sql= """
    SELECT collections.collectionID,  collections.collectionName,  collectionItems.itemID 
    FROM collections, collectionItems
    WHERE  collections.collectionID =  collectionItems.collectionID    ;
    """

    query = cur.execute(sql)
    rows = query.fetchall()
    return rows



def get_item_from_collections( collid ):
    """
    Return list of all itemID from some collection, 
    given the collectionID

    """

    sql= """
    SELECT  collectionItems.itemID 
    FROM collections, collectionItems
    WHERE      collections.collectionID =  collectionItems.collectionID 
           AND collectionItems.collectionID = ? ;       
    """                        

    query=cur.execute(sql,(collid,))        
    rows=query.fetchall()       

    itemids = [ ]


    for row in rows:
        itemid = row[0]
        itemids = itemids + [itemid]

    return itemids




def list_tags():
    """
    #print all zotero tags

    @type  void
    @param void
    @rtype void 

    """
    rows = get_tags()

    for row in rows:
        tagID, tag = row
        #print str(tagID) + "\t" + tag



def list_collections():
    """
    #print all Zotero collections

    """

    rows = get_collections()

    for row in rows:
        collID, collection = row
        #print str(collID) + "\t" + collection


def get_item_ids():
    """
    Return the itemID of all items
    """

    sql = """
    SELECT itemID FROM items 
    ORDER BY itemID
    ;
    """

    itemids = [ ]

    query=cur.execute(sql)   
    rows =query.fetchall()

#    print rows

    for row in rows:
        itemid = row[0]
        itemids = itemids + [itemid]

    return itemids         


def get_items():
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

    query=cur.execute(sql)  
    rows=query.fetchall()

    return rows


def list_items():
    """
    #print all items in zotero library.

    """

    
    rows = get_items()

    for row in rows:
        itemID , itemName = row
        #print str(itemID) + "\t" + itemName



def filter_tag(tagid):
       """
       Filter item by tags
       """


       sql = """
       SELECT itemTags.itemID  
       FROM itemTags
       WHERE itemTags.tagID = ?
       ;

       """

       query=cur.execute(sql,(tagid,))        
       rows=query.fetchall()

       itemids = []

       for row in rows:
           itemid = row[0]
           itemids = itemids + [itemid]

       return itemids     

        



def get_item_data(itemid):

    sql = """

    SELECT  fields.fieldName , itemDataValues.value  

    FROM      itemData, itemDataValues  , fields

    WHERE   itemData.valueID =  itemDataValues.valueID AND 
        fields.fieldID = itemData.fieldID  	   AND
        itemData.itemID = ?

    """
    query=cur.execute(sql,(itemid,))   
    rows=query.fetchall()

    return rows



def list_item_data(itemid):

    rows = get_item_data(itemid)

    for row in rows:
        data_type , value = row
        print data_type + "\t\t" + value + "\n"



def get_item_attachment(itemid):
    sql = """
    SELECT    items.key, itemAttachments.path 
    FROM      items,     itemAttachments
    WHERE   items.itemID = itemAttachments.itemID AND items.itemID = ?
    ORDER BY items.itemID  
    ;    
    """
    query=cur.execute(sql,(itemid,))
    row=query.fetchall()

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
            ffile =  os.path.join(STORAGE_PATH,dirr,name)
            print ffile
        else:
            return -1

        return ffile



def get_attachment(itemid):
    
    sql= """ 
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

    query = cur.execute(sql,(itemid,))
    rows = query.fetchall()

    ##print rows

    if rows == []:
        return None

    data = rows[0]

    key  = data[1]

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

        data2= get_attachment(itemid+1);
#        #print "data2 ="
#        #print data2
        return data2

    ##print "tr3"

    fname = path.split("storage:")[1]
    PATH = os.path.join(STORAGE_PATH, key,fname)
    ##print PATH

    return PATH
                                  

# Close database connection
#conn.close()

if __name__=="__main__":

    #print "Testing"

    open_database(DATABASE2);
    #list_items();


