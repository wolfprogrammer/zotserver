#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module program description
	1. This program does
	2. The user interface is ....

"""    

PORT=8080	#: Sets the default port
HOST='0.0.0.0'  #: Accept anyhost  
DEBUG= True     #: True - Debug ON
#HOST='0.0.0.1' # Local host only


from bottle import static_file, abort
from bottle import route, run, debug
from bottle import template, request, post, get
from bottle import validate, static_file      

from  zoterotool import *


open_database(DATABASE2);



def link_tpl(url,name,conf=0):
    """
    Create html link code to URL
    Returns the html code to the link

    conf=0 : Any link
    conf=1 : Internal file

    """

    if conf ==1:
         url="/files" + url

    link = '<a href="' + url + '">' + name + '</a>'  
    return link
    



def get_item_link(itemid):
    """
    Returns a html link to the file, given the fileID

    """
    # Get item attachment path
    #path =  get_item_attachment(itemid)
    path =  get_attachment(itemid)
 
    if path is not None:
        #path = os.path.join("/files", path)
        #path = "/files" + path

        name = os.path.split(path)[1]        
        link = link_tpl( path, name,1 )
        print link


        #link = '<a href="' + path + '">' + "file" + "</a>"


        return link    

    return None



def print_all_links():
    items =  get_items()

    linklist = ""

    for item in items:
        itemId, itemName = item
        print str(itemId) 
        print itemName
      
        path =  get_item_attachment(itemId)
        if path is not None and path != -1 :
            print "path = " +  path
            link = link_tpl(path,itemName,1)

            linklist= linklist + link + "\n " + "<br />"
            print link

    return linklist



@route('/')
def index():
    return link_tpl("/items","All zotero collection items")




@route('/items')
def all_items():
    """
    In this page all Zotero collection
    items are printed with a download 
    link.

    """

    links =  print_all_links()
    return links
          

@route('/collections')
def all_collections():
    """
    Show the user all Zotero collections 
    with a link to the items in the collections

    Page code
    ---------
    link-to-collection-id1    http://site-host/collectionid/id1
    link-to-collection-id2 :  http://site-host/collectionid/id2
    ...
    ...

    """

    collections = get_collections()

    html = ""

    
    for coll in collections:
        collid, collname = coll

        print "collid " + str(collid)
        
        url   = "/collectionid/" + str(collid)
        link  = link_tpl(url,collname)

        html = html + link + "<br />\n"

    return html
        

@route('/collectionid/<collid:int>')
def show_collection(collid):

    itemIDs= get_item_from_collections(collid)

    print itemIDs

    type(itemIDs)

    html = ""

    print "show_collection Debug Trace ----------__"

    for itemid in itemIDs:

        link = get_item_link(itemid)


        if link is not None:
            html = html + link + "<br />\n"

            print "link " + link
            print "itemid " + str(itemid)


#    return "The collection was: %s" % str(collid)

    return html



@route('/files/<path:path>')
def callback(path):

    path=os.path.join("/",path)


    print "path =" + path
    if os.path.isfile( path ):
        path_, file_ = os.path.split(path)

        print "retriving"
        print "path " + path_
        print "filename =" + file_

        return static_file(file_, path_ )
    else:
        return "Error: File don't exist on server."



# Run the server 
if __name__=="__main__":     
    run(host=HOST, port=PORT, debug=DEBUG, reloader=True)   
          

