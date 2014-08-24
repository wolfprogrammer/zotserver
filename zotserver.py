#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Module program description
1. This program does
2. The user interface is ....

"""
import os
from Config import Config
from bottle import static_file, abort, redirect
from bottle import route, run, debug
from bottle import template, request, response, post, get
from bottle import static_file
from zoterotool import Zotero

from Logger import logger


PORT = Config.PORT
HOST = Config.HOST
DEBUG = Config.DEBUG

zotero = Zotero(Config.DATABASE, Config.STORAGE)


def link_tpl(url, name, linktofile=False, newtab=False):
    """
    Create html link code to URL
    Returns the html code to the link

    linktofile = False : Link to any page
               = True  : Link to Internal file

    newtab     = False : Open the links in same tab/window
                 True  : Force to open links in new tab
    """

    if linktofile == True:
        url = "/files/" + url

    targ = ""
    if newtab == True:
        targ = ' target="_blank" '

    link = '<a href="' + url + '"' + targ + '>' + name + '</a>'
    return link


def get_item_link(itemid):
    """
    Returns a html link to the file, given the fileID

    """
    # Get item attachment path
    # path =  get_item_attachment(itemid)
    path = zotero.get_attachment(itemid)

    if path is not None:
        # path = os.path.join("/files", path)
        # path = "/files" + path

        name = os.path.split(path)[1]
        link = link_tpl(path, name, linktofile=True, newtab=True)
        # print link
        # link = '<a href="' + path + '">' + "file" + "</a>"
        return link

    return None


def link_list_tpl(url_list):
    """
    Generates a html code of a  list of links 
    given a list of URL

    url_list = [ [ "URL1", "Description1"] , [ "URL2", "description2" ] .... ]

    """

    html = ""

    for url_ in url_list:
        url, name = url_
        link = link_tpl(url, name)
        html = html + "*" + link + "<br />\n"

    return html


def html_item_link_list(itemIDs):
    """
    Creates a html code of link to the library Items,
    given the item ID

    Input: itemIDs:  list of integer values itemID

    """

    html = ""

    for itemid in itemIDs:

        link = get_item_link(itemid)

        if link is not None:
            html2 = item_data_html(itemid)
            html = html + link + "<br />" + html2 + "<br /><br />\n"

    return html


def item_data_html(itemid):
    """
    Returns item data in html format

    """
    data = zotero.get_item_data(itemid)

    html = ""

    for dat in data:
        html = html + "%s\t\t%s <br />\n " % ( dat[0], dat[1] )

    return html


def format_query(query):
    """
    Given    query=" word1 word2 word3
    Returns  " word1 OR word2 OR word3"

    """
    words = query.split()
    # print words

    text = ""
    for idx in range(len(words) - 1):
        text = text + words[idx] + " OR "

    text = text + words[-1]
    return text


def html_collections_link(collections):
    """
    Return a html code of a collection 

    collections_list = [ ( collIDd, collName ,) ... ]
    [ (1 , "col1") , ( 4, "coll2" ) , ... ]

    """

    html = ""
    for coll in collections:
        collid, collname = coll

        url = "/collectionid/" + str(collid)
        link = link_tpl(url, collname)

        html = html + link + "<br />\n"

    # print html
    return html


@route('/index')
@route('/')
def index():
    # link_list   =  link_list_tpl(\
    # [\
    # [ "/items", "Items"             ] ,\
    # [ "/tags", "Tags"               ] ,\
    # [ "/collections", "Collections" ] ,\
    # [ "/status","Server Status"     ] ,\
    # [ "/help","Help"                ] ])

    logger.warn("ROUTE: /index")

    search_form = '''
    <br />
    <form action="/search" method="GET">
            Search Library <br /><input name="q" type="text" autofocus />
            <input value="Search" type="submit" />
        </form>
    '''

    update_button = '''
    <br /><br />
    <form action="/updatelib" method="post">    
        <input value="Update Library" type="submit" />
    </form>
    '''

    #    content_ =  link_list + search_form + update_button
    content_ = search_form + update_button
    return template("base.html", subtitle="Options:", content=content_, backlink="index")


@post('/updatelib')
def updatelibrary():
    logger.warn("ROUTE: /updatelib")
    # os.system("./update-data.sh")
    # open_database("zotero.sqlite");
    # create_text_index()
    redirect("/index")


@route('/items')
def all_items():
    """
    In this page all Zotero collection
    items are printed with a download 
    link.

    """
    logger.warn("ROUTE: /items")
    items = zotero.get_item_ids()

    html = html_item_link_list(items)

    return template("base.html", subtitle="Items", content=html, backlink="index")


@route('/all_collections')
def all_collections_():
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
    logger.warn("ROUTE: /all_collections")
    collections = zotero.get_collections()

    html = html_collections_link(collections)

    return template("base.html", subtitle="Collections", content=html, backlink="index")


@route('/collections')
def collections_():
    """
    Show links to the parent collections

    """
    logger.warn("ROUTE: /collections")
    collections = zotero.get_collections_parents()
    html = html_collections_link(collections)
    return template("base.html", subtitle="Collections", content=html, backlink="index")


@route('/collectionid/<collid:int>')
def show_collection(collid):
    # Find all subcollections from a given collecion
    # which  collID is known.
    #
    # subcollections =  [ ( collIDx, collNameX ), ( ....) ... ]
    #
    logger.warn("ROUTE: /collectionid/<collid:int> = %s" % collid )

    subcollections = zotero.get_subcollections(collid)
    html_subcolls = html_collections_link(subcollections)

    collname = zotero.get_collection_name(collid)

    items = zotero.get_item_from_collections(collid)

    html_items = html_item_link_list(items)

    html = html_subcolls + '\n<hr width=35% color="black" align="left" >\n'
    html = html + html_items

    subtilte_ = "Collection: " + collname
    return template("base.html", subtitle=subtilte_, content=html, backlink="collections")


@route('/fileid/<itemid:int>')
def retrive_file(itemid):
    """
    Retrives file that matches itemid

    """
    logger.warn("ROUTE: /fileid = %s" % itemid)

    path = zotero.get_attachment(itemid)
    if path is not None:
        path_, file_ = os.path.split(path)

        # print path_
        # print file_

        return static_file(file_, path_, download=file_)
    # return "File was  " + str(itemid) + " " + path
    else:
        return "Error: File not found"


@route('/files/<path:path>')
def callback(path):
    logger.warn("ROUTE: /file = %s" % path)
    # path=os.path.join("/",path)
    # print path

    # print "path =" + path
    if os.path.isfile(path):
        path_, file_ = os.path.split(path)

        # print "retriving"
        # print "path " + path_
        # print "filename =" + file_

        return static_file(file_, path_)
    else:
        return "Error: File don't exist on server."


@route('/tags')
def show_tags():
    """
    In this page all tags are showed
    when some tag is clicked only the files
    related to this tag will be showed to the user
    
    """
    logger.warn("ROUTE: /tags")
    html = ""

    tags = zotero.get_tags()
    for tag in tags:
        tagid, tagname = tag

        url = "/tagid/" + str(tagid)
        # print url
        link = link_tpl(url, tagname)

        html = html + link + "<br />\n"

    return template("base.html", subtitle="Tags", content=html, backlink="index")


@route('/tagid/<tagid:int>')
def show_tagid(tagid):
    logger.warn("ROUTE: /tagid = %s" % tagid)

    tagname = zotero.get_tagname(tagid)
    items = zotero.filter_tag(tagid)
    html = html_item_link_list(items)
    subtilte_ = "Tag: " + tagname
    return template("base.html", subtitle=subtilte_, content=html, backlink="tags")

# @route('/query')
# def query_libray(query):
# """
# Full text search in the database

# http://<base url>/search-expression

# """

##    itemids = text_search(query)
##    html = html_item_link_list( itemids )
##    return html
#return query

last_query = ""


@route('/search')
def search_library():
    query = request.params.get('q')
    last_query = query

    logger.warn("ROUTE: /Search")
    print "query " + query

    html = ""

    #    import ipdb; ipdb.set_trace()


    if query != "":
        query = format_query(query)
        itemids = zotero.text_search(query)
        html = html_item_link_list(itemids)

    search_form = '''
    <br />
    <form action="/search" method="GET">
            Search Library <br /><input name="q" type="text" value="%s" autofocus />
            <input value="Search" type="submit" />
        </form>
    <br />            
    '''

    search_form = search_form % ( last_query )

    content_ = search_form + html
    return template("base.html", subtitle="Search Library", content=content_, backlink="index")


#   return 'Your query value was: {}'.format(query)


@route("/status")
def status():
    """
    Shows the status of the server
    """
    import subprocess
    logger.warn("ROUTE: /status")

    response.content_type = "text/plain"
    return subprocess.check_output(["cat", "/tmp/zotserver.log"])


@route("/help")
def help():
    logger.warn("ROUTE: help")

    html = \
        """
    The ZOTERO SERVER - Is a http web server that uses bottle framework. <br />
    This simple and lightweight web server allows to access the Zotero   <br />
    data from anywhere, any device, tablet, smartphone, PC ...           <br />
    """

    return template("base.html", subtitle="HELP", content=html, backlink="index")


@get('/favicon.ico')
def get_favicon():
    logger.warn("ROUTE: /favicon")
    return static_file('favicon.ico', ".")


def main():
    data = {"PORT": PORT, "HOST": HOST}
    logger.warn("Starting server %s" % data)
    run(host=HOST, port=PORT, debug=DEBUG, reloader=True)


# Run the server 
if __name__ == "__main__":
    main()
