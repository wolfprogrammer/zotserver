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



# Paths
HOME = os.path.expanduser("~/")
PATH= HOME + "zotero-server/"
STORAGE_PATH= PATH + "storage/"

print PATH

#  Create a copy of zotero database due to lock issues.
#
DATABASE1=  PATH + "zotero.sqlite"
DATABASE2 = PATH + "zotero.sqlite"

print DATABASE2

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


    #print rows
    return rows



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



def list_tags():
    """
    Print all zotero tags

    @type  void
    @param void
    @rtype void 

    """
    rows = get_tags()

    for row in rows:
        tagID, tag = row
        print str(tagID) + "\t" + tag



def list_collections():
    """
    Print all Zotero collections

    """

    rows = get_collections()

    for row in rows:
        tagID, tag = row
        print str(tagID) + "\t" + tag


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
    Print all items in zotero library.

    """

    
    rows = get_items()

    for row in rows:
        itemID , itemName = row
        print str(itemID) + "\t" + itemName



def filter_tag(tagid):
       """
       Filter item by tags
       """


       sql = """
       SELECT itemTags.itemID, item_names.value

       FROM   itemTags, tags  , item_names

       WHERE  itemTags.tagID = tags.tagID  AND  
          item_names.itemID = itemTags.itemID AND tags.tagID= ?
       ;

       """

       query=cur.execute(sql,(tagid,))        
       rows=query.fetchall()

       print rows


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

    for row in rows:
        data_type , value = row
        print str(data_type) + "\t\t" + str(value) + "\n"



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

        print type(dirr)
        print type (name)

        if name is not None:
            name = name.split("storage:")[1]
        else:
            return -1
        
        if dirr is not None:
            ffile = STORAGE_PATH + dirr + "/" + name
        else:
            return -1

        return ffile






# Close database connection
#conn.close()

if __name__=="__main__":

    print "Testing"

    open_database(DATABASE2);
    list_items();


