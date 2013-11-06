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



def create_url(url,name,conf=0):
    """
    Create html link code to URL
    Returns the html code to the link

    conf=0 : Any link
    conf=1 : Internal file

    """

    if conf ==1:
         #url= os.path.join("/files", url)
         url="/files" + url

    link = '<a href="' + url + '">' + name + '</a>'  
#    print link

    return link
    



def get_item_link(itemid):
    """
    Returns a html link to the file

    """
    # Get item attachment path
    path =  get_item_attachment(itemid)
 
    
    path = os.path.join("/files", path)
    link = '<a href="' + path + '">' + "file" + "</a>"
    #print link 
    return link



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
            link = create_url(path,itemName,1)

            linklist= linklist + link + "\n " + "<br />"
            print link

    return linklist



@route('/')
def index():

    #return '<a href="/static/8_IAPM_final.pdf">filename</a>'

#    return '<a   href="/static/../../zotero-server/storage/FK9M5HDF/8_IAPM_final.pdf">file</a>'

    links =  print_all_links()
    return links
#    return get_item_link(243)
          


@route('/download/:filename')
def download(filename):
    pwd = os.getcwd()

    print filename
    return static_file(filename, root=pwd, download=filename)    


@route('/staticxx/:filename')
def server_static(filename):
    pwd = os.getcwd()


    if os.path.isfile( filename):
        path, basename = os.path.split(filename)
    else:
        abort(401, "Error: File not found in the server")

#    return " %s %s %s  " % ( filename , path, basename )
    return static_file(basename, root=path)



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



#    return  path     



#@route('/static/<url:re:.+>:') 
#@route('/static/:<url>') 
@route('/staticy/:filename#.*#')    
def sever_file(filename):
    print filename ; 
    pwd = os.getcwd()


    if os.path.isfile( filename ):
        path, basename = os.path.split(filename)
        print "path " + path
        print "basename =" + basename
    else:
        print "Error"
        abort(401, "Error: File not found in the server")

#    return " %s %s %s  " % ( filename , path, basename )
    return static_file(basename, root=path, download=basename)
 


# Run the server 
run(host=HOST, port=PORT, debug=DEBUG, reloader=True)   
          

