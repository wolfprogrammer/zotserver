#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Zotsever.py

Zotserver main file. To change configurations. Change the file zotserver.conf
directories and database location.

1 - First edit and run ./scripts/update.sh
2 - Change zotserver.conf paths to storage location of zotero files and datbase
3 - Run ./zotserver.py


"""
import os

from bottle import Bottle
from bottle import static_file, abort, redirect
from bottle import route, run, debug
from bottle import template, request, response, post, get
from bottle import static_file
from zoterolib import Zotero
from PyLib import Config, logger, request_logger, get_resource_file, get_resource_path

PORT = Config.PORT
HOST = Config.HOST
DEBUG = Config.DEBUG
RELOAD = Config.RELOAD
SERVER = Config.SERVER

zotero = Zotero(Config.DATABASE, Config.STORAGE, Config.ZOTDIR)

favicon = get_resource_path('templates/favicon.ico')
base_template = get_resource_path("templates/base.html")

app = Bottle()

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

def item_link_tpl(path, name, newtab=True):
    """
    Create html link code to URL
    Returns the html code to the link

    linktofile = False : Link to any page
               = True  : Link to Internal file

    newtab     = False : Open the links in same tab/window
                 True  : Force to open links in new tab
    """

    url = os.path.join("/library/", os.path.relpath(path, zotero.storage))
    logger.debug("url = %s" % url)

    targ = ""
    if newtab == True:
        targ = ' target="_blank" '

    link = "".join(['<a href="', url, '"', targ, '>', name, '</a>'])
    logger.debug("link = %s" % link)
    return link



def get_item_link(itemid):
    """
    Returns a html link to the file, given the fileID

    """
    # Get item attachment path
    # path =  get_item_attachment(itemid)
    path = zotero.get_attachment(itemid)

    logger.debug("path = %s" % path)

    if path is not None:
        # path = os.path.join("/files", path)
        # path = "/files" + path

        name = os.path.split(path)[1]
        link = item_link_tpl(path, name, newtab=True)
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
        logger.debug("itemid = %s" % itemid)
        logger.debug("link = %s" % link)

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


#-------------------------------#
#         R O U T E S           #
#-------------------------------#


@app.route('/index')
@app.route('/')
def route_index():
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
    return template(base_template, subtitle="Options:", content=content_, backlink="index")


@app.post('/updatelib')
def route_updatelib():
    logger.warn("ROUTE: /updatelib")
    # os.system("./update.sh")
    # open_database("zotero.sqlite");
    zotero.create_text_index()
    redirect("/index")


@app.route('/items')
def route_items():
    """
    In this page all Zotero collection
    items are printed with a download 
    link.

    """
    logger.warn("ROUTE: /items")
    items = zotero.get_item_ids()

    html = html_item_link_list(items)

    return template(base_template, subtitle="Items", content=html, backlink="index")


@app.route('/all_collections')
def route_all_collections_():
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

    return template(base_template, subtitle="Collections", content=html, backlink="index")


@app.route('/collections')
def route_collections():
    """
    Show links to the parent collections

    """
    logger.warn("ROUTE: /collections")
    collections = zotero.get_collections_parents()
    html = html_collections_link(collections)
    return template(base_template, subtitle="Collections", content=html, backlink="index")


@app.route('/collectionid/<collid:int>')
def route_collectionid(collid):
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
    return template(base_template, subtitle=subtilte_, content=html, backlink="collections")


@app.route('/fileid/<itemid:int>')
def route_fileid(itemid):
    """
    Retrives file that matches itemid

    """
    logger.warn("ROUTE: /fileid = %s" % itemid)
    path = zotero.get_attachment(itemid)
    logger.debug("path = %s" % path)

    if path is not None:
        path_, file_ = os.path.split(path)

        logger.debug("path_ = %s" % path_)
        logger.debug("file_ = %s" % file_)

        return static_file(file_, path_, download=file_)
    # return "File was  " + str(itemid) + " " + path
    else:
        return "Error: File not found"


@app.route('/files/<path:path>')
def route_files(path):
    logger.warn("ROUTE: /files = %s" % path)

    if os.path.isfile(path):
        path_, file_ = os.path.split(path)

        logger.debug("path_ = %s" % path_)
        logger.debug("file_ = %s" % file_)

        return static_file(file_, path_)
    else:
        logger.debug("Error: File don't exist on server.")
        return "Error: File don't exist on server."

@app.route('/library/<path:path>')
def route_library(path):
    logger.warn("ROUTE: /files = %s" % path)

    _path = os.path.join(zotero.storage, path)

    if os.path.isfile(_path):
        path_, file_ = os.path.split(_path)

        logger.debug("path_ = %s" % path_)
        logger.debug("file_ = %s" % file_)

        return static_file(file_, path_)
    else:
        logger.debug("Error: File don't exist on server.")
        return "Error: File don't exist on server."


@app.route('/tags')
def route_tags():
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
        link = link_tpl(url, tagname)
        html = html + link + "<br />\n"

    return template(base_template, subtitle="Tags", content=html, backlink="index")


@app.route('/tagid/<tagid:int>')
def route_tagid(tagid):
    logger.warn("ROUTE: /tagid = %s" % tagid)

    tagname = zotero.get_tagname(tagid)
    items = zotero.filter_tag(tagid)
    html = html_item_link_list(items)
    subtilte_ = "Tag: " + tagname
    return template(base_template, subtitle=subtilte_, content=html, backlink="tags")

last_query = ""

@app.route('/search')
def route_search():
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
    return template(base_template, subtitle="Search Library", content=content_, backlink="index")

#   return 'Your query value was: {}'.format(query)
@app.route("/status")
def route_status():
    """
    Shows the status of the server
    """
    import subprocess
    logger.warn("ROUTE: /status")

    response.content_type = "text/plain"
    return open(Config.LOG,"r").read()

@app.route("/help")
def route_help():
    logger.warn("ROUTE: help")

    html = \
    """
    The ZOTERO SERVER - Is a http web server that uses bottle framework. <br />
    This simple and lightweight and self contained web server allows to access the     <br />
    Zotero data from anywhere or from anywhere, any device, tablet, smartphone, PC ... <br />

    See updates on: %s
    """
    link = link_tpl("https://github.com/wolfprogrammer/zotserver", "Zotserver Repository"
                    ,linktofile=False, newtab=True)
    html = html % link

    return template(base_template, subtitle="HELP", content=html, backlink="index")


@app.get('/favicon.ico')
def get_favicon():
    logger.warn("ROUTE: /favicon")
    return static_file(favicon, ".")


import datetime

# unchanged from OP
def log_after_request():
    try:
        length = response.content_length
    except:
        try:
            length = len(response.body)
        except:
            length = '???'
    print 'MYLOG:', '{ip} - - [{time}] "{method} {uri} {protocol}" {status} {length}'.format(
        ip=request.environ.get('REMOTE_ADDR'),
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        method=request.environ.get('REQUEST_METHOD'),
        uri=request.environ.get('REQUEST_URI'),
        protocol=request.environ.get('SERVER_PROTOCOL'),
        status=response.status_code,
        length=length,
    )


class AccessLogMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, e, h):
        # call bottle and store the return value
        ret_val = self.app(e, h)

        try:
            length = response.content_length
        except:
            try:
                length = len(response.body)
            except:
                length = '???'

        # log the request
        #log_after_request()
        ip=request.environ.get('REMOTE_ADDR'),
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        method=request.environ.get('REQUEST_METHOD'),
        uri=request.environ.get('REQUEST_URI'),
        protocol=request.environ.get('SERVER_PROTOCOL'),
        status=response.status_code,
        length=length,

        request_logger.info("ip {ip} method {method} uri {uri} protocol {protocol} status {status} lenght {lenght}".format
                            (ip=ip,
                             method= method,
                             uri=uri,
                             protocol=protocol,
                             status=status,
                             lenght=length
                             ))

        # return bottle's return value
        return ret_val

logged_app = AccessLogMiddleware(app)

def main():
    data = {"PORT": PORT, "HOST": HOST}
    logger.warn("Starting server %s" % data)

    run(app=logged_app, host=HOST, port=PORT,  server=SERVER , debug=DEBUG, reloader=RELOAD)


# Run the server 
if __name__ == "__main__":
    main()
