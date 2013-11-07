#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module program description
	1. This program does
	2. The user interface is ....

"""    

PORT=8080	#: Sets the default port

HOST='0.0.0.0'  #: Accept anyhost  
#HOST='127.0.0.1' # Local host only

#DEBUG= True     #: True - Debug ON
DEBUG= False


from bottle import static_file, abort, redirect
from bottle import route, run, debug
from bottle import template, request, response, post, get
from bottle import validate, static_file      

from  zoterotool import *


open_database("zotero.sqlite");


def link_tpl(url,name,conf=0):
    """
    Create html link code to URL
    Returns the html code to the link

    conf=0 : Any link
    conf=1 : Internal file

    """

    if conf ==1:
         url="/files/" + url

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
        #print link


        #link = '<a href="' + path + '">' + "file" + "</a>"


        return link    

    return None



def print_all_links():
    items =  get_items()

    linklist = ""

    for item in items:
        itemId, itemName = item
        #print str(itemId) 
        #print itemName
      
        path =  get_item_attachment(itemId)
        if path is not None and path != -1 :
            #print "path = " +  path
            link = link_tpl(path,itemName,1)

            linklist= linklist + link + "\n " + "<br />"
            #print link

    return linklist



def link_list_tpl ( url_list ):
    """
    Generates a html code of a  list of links 
    given a list of URL

    url_list = [ [ "URL1", "Description1"] , [ "URL2", "description2" ] .... ]

    """

    html = ""

    for url_ in url_list:

        url, name = url_
        link = link_tpl(url, name)
        html = html + "*" + link  + "<br />\n"

    return html


@route('/index')
@route('/')
def index():  

    link_list   =  link_list_tpl(\
            [\
            [ "/items", "Items"             ] ,\
            [ "/tags", "Tags"               ] ,\
            [ "/collections", "Collections" ] ,\
            [ "/status","Server Status"     ] ,\
            [ "/help","Help"                ] ])

    button = '''
    <br /><br />
    <form action="/updatelib" method="post">    
        <input value="Update Library" type="submit" />
    </form>
    '''                                             
  
    content_ =  link_list + button
    return template("base.html", subtitle="Options:", content= content_ , backlink = "index" )


@post('/updatelib')
def updatelibrary():
    global conn

    os.system("./update-data.sh")
    close_database()
    open_database("zotero.sqlite");
    redirect("/index")




@route('/items')
def all_items():
    """
    In this page all Zotero collection
    items are printed with a download 
    link.

    """

    links =  print_all_links()
    return template("base.html", subtitle="Items", content= links, backlink="index" )
#    return links
          

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

        #print "collid " + str(collid)
        
        url   = "/collectionid/" + str(collid)
        link  = link_tpl(url,collname)

        html = html + link + "<br />\n"


#   links =  print_all_links()
    return template("base.html", subtitle="Collections", content= html, backlink="index" )  
#    return html
        



@route('/collectionid/<collid:int>')
def show_collection(collid):


    collname = get_collection_name(collid)

    itemIDs= get_item_from_collections(collid)

    #print itemIDs


    html = ""

    #print "show_collection Debug Trace ----------__"

    for itemid in itemIDs:

        link = get_item_link(itemid)


        if link is not None:
            html = html + link + "<br />\n"

            #print "link " + link
            #print "itemid " + str(itemid)

    subtilte_ = "Collection: " + collname
    return template("base.html", subtitle= subtilte_ , content= html, backlink="collections" )   


@route('/fileid/<itemid:int>')
def retrive_file(itemid):
    """
    Retrives file that matches itemid

    """

    path = get_attachment(itemid)
    if path is not None:
        path_, file_ = os.path.split(path)   

        #print path_
        #print file_

        return static_file(file_, path_, download = file_ ) 
#       return "File was  " + str(itemid) + " " + path
    else:
        return "Error: File not found"


        

@route('/files/<path:path>')
def callback(path):

    #path=os.path.join("/",path)
    #print path

    #print "path =" + path
    if os.path.isfile( path ):
        path_, file_ = os.path.split(path)

        #print "retriving"
        #print "path " + path_
        #print "filename =" + file_

        return static_file(file_, path_ )
    else:
        return "Error: File don't exist on server."


@route('/tags')
def show_tags():
    """
    In this page all tags are showed
    when some tag is clicked only the files
    related to this tag will be showed to the user
    
    """

    html = ""

    tags = get_tags()
    for tag in tags:

        tagid, tagname = tag

        url =   "/tagid/" + str(tagid)
        #print url
        link = link_tpl(url,tagname)

        html = html + link + "<br />\n"


    return template("base.html", subtitle="Tags", content= html, backlink="index" )  
#    return html


@route('/tagid/<tagid:int>')
def show_tagid(tagid):

    tagname = get_tagname(tagid)

    itemIDs = filter_tag(tagid)


    html = ""
    for itemid in itemIDs:

        link = get_item_link(itemid)


        if link is not None:
            html = html + link + "<br />\n"

    subtilte_ = "Tag: " + tagname
    return template("base.html", subtitle= subtilte_ , content= html, backlink="tags" ) 


@route("/status")
def status():
    """
    Shows the status of the server
    """
    import subprocess
    
    response.content_type = "text/plain"
    return subprocess.check_output(["cat", "/tmp/zotserver.log"])



@route("/help")
def help():

    html = """
    The ZOTERO SERVER - Is a http web server that uses bottle framework. <br />
    This simple and lightweight web server allows to access the Zotero   <br />
    data from anywhere, any device, tablet, smartphone, PC ...           <br />
    

    """

    return template("base.html", subtitle= "HELP" , content= html , backlink="index" ) 




@get('/favicon.ico')
def get_favicon():
#    return server_static('favicon.ico')
    return static_file('favicon.ico', "." )     


# Run the server 
if __name__=="__main__":     
    run(host=HOST, port=PORT, debug=DEBUG, reloader=True)   
          

