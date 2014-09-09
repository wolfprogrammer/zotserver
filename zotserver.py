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
from PyLib import Config, logger, request_logger, get_resource_file, get_resource_path, this_dir
import py2html


IMAGEMAGICK="convert"

PORT = Config.PORT
HOST = Config.HOST
DEBUG = Config.DEBUG
RELOAD = Config.RELOAD
SERVER = Config.SERVER

zotero = Zotero(Config.DATABASE, Config.STORAGE, Config.ZOTDIR)

favicon = get_resource_path('resource/favicon.ico')
base_template = get_resource_path("resource/base.html")

app = Bottle()

from subprocess import Popen, PIPE


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

    #link = '<a href="{url}" {targ}> {name} </a>'.format(url=url, targ=targ, name=name)

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



def get_item_link(item_filename):
    """
    Returns a html link to the file, given the fileID

    """
    # Get item attachment path

    path = item_filename #zotero.get_attachment(itemid)
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


def item_picture(itemID):
    """
    :return:
    """
    filepath = zotero.get_attachment(itemID)

    try:
        #print "filepath = %s" % filepath

        path, filename = os.path.split(filepath)
    except:
        return None
    coverfile = os.path.join(path, "filecover.jpeg")

    if filepath.endswith('.pdf'):

        # Test if pdf cover file exists in
        # its storage directory
        if not os.path.exists(coverfile):
            #print "Creating file %s" % coverfile

            pwd = os.getcwd()
            os.chdir(path)
            #print "command = ", ", ".join([IMAGEMAGICK, '\"%s\"[0]' % filename, "filecover.jpeg"])
            p = Popen(" ".join([IMAGEMAGICK, '-thumbnail x300', '\"%s\"[0]' % filename, "filecover.jpeg"]), shell=True)
            p.wait()
            os.chdir(pwd)

        return coverfile
    return None



def html_item_link_list(itemIDs):
    """
    Creates a html code of link to the library Items,
    given the item ID

    Input: itemIDs:  list of integer values itemID

    """

    html = ""

    for itemid in itemIDs:

        filepath = zotero.get_attachment(itemid)
        itemlink = get_item_link(filepath)

        if filepath is None:
            continue

        picture = item_picture(itemid)

        item_tags = zotero.get_item_tags(itemid)

        item_tag_links = [link_tpl("/tagid/%s" % tagid, tagname) for tagid, tagname in item_tags]
        item_tag_links = " ".join(item_tag_links)
        related_tags = "Tags: %s<br />" % item_tag_links

        # print "item_tag_links = ", str(item_tag_links)
        # print "type = ",type(item_tag_links)

        logger.debug("itemid = %s" % itemid)
        logger.debug("picture = %s" % picture)
        logger.debug("filepath = %s" % filepath)
        logger.debug("itemlink = %s" % itemlink)


        if picture is not None:


            if picture is not None:
                src="/coverid/%s" % itemid
                image_html = py2html.html_image(src="/coverid/%s" % itemid,
                                                width=240, height=180, href=src)
                #image_html = "".join(['<br />', image_html, '<br />'])
        else:
            image_html = ""

        html_data = item_data_html(itemid)

        _table = py2html.html_table([[itemlink], [html_data], [related_tags]], cellspacing=2)
        table = py2html.html_table([[image_html,_table]])

        #logger.debug("table = %s" % table)

        html = "<br />\n".join([html, table])

        logger.debug("html = \n%s" % html)
            #html = "<br />\n".join([html, itemlink, related_tags, html_data, image_html])

    return html


def item_data_html(itemid):
    """
    Returns item data in html format

    """
    data = zotero.get_item_data(itemid)
    logger.debug("data = %s" % data)

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


def create_thumbnails():

    itemIDS = zotero.get_item_ids()


    for itemID in itemIDS:
        try:
            filepath = zotero.get_attachment(itemID)
            logger.debug("Creating thumbnail %s" % filepath)
            print "thumbnail %s" % filepath

            path, filename = os.path.split(filepath)

            if filepath.endswith('.pdf'):

                pwd = os.getcwd()
                os.chdir(path)
                p = Popen(" ".join([IMAGEMAGICK, '-verbose -density 150  -quality 100  -trim', '\"%s\"[0]' % filename, "filecover.jpeg"]), shell=True)
                p.wait()
                os.chdir(pwd)
        except Exception as err:
            print err, err.args, err.__class__

#-------------------------------#
#         R O U T E S           #
#-------------------------------#


@app.route('/index')
@app.route('/')
def route_index():

    logger.warn("ROUTE: /index")
    redirect("/collections")
    #return template(base_template, subtitle="Options:", content="", backlink="index")

@app.post('/updatelib')
def route_updatelib():
    logger.warn("ROUTE: /updatelib")
    from subprocess import Popen, PIPE

    script = os.path.join(this_dir(), 'scripts/update.sh')

    logger.warn("Executing %s" % script)

    update_log = os.path.join(Config.ZOTDIR, 'log', "update.log")
    out_err = Popen([script], stdout=PIPE, stderr=PIPE).communicate()
    open(update_log, 'w').write("".join(out_err))

    # os.system("./update.sh")
    # open_database("zotero.sqlite");
    zotero.create_text_index()
    create_thumbnails()
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

    html = html_subcolls + "<br \><br />"# + '\n<hr width=35% color="black" align="left" >\n'
    html = html + html_items

    logger.debug("collname = %s" % collname)
    logger.debug("items = %s" % items)
    logger.debug("html_items %s" %html_items )

    subtilte_ = "Collection: " + collname
    return template(base_template, subtitle=subtilte_, content=html, backlink="collections")


@app.route('/collection/<name>')
def route_collection(name):
    return name




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


# @app.route('/files/<path:path>')
# def route_files(path):
#     logger.warn("ROUTE: /files = %s" % path)
#
#     if os.path.isfile(path):
#         path_, file_ = os.path.split(path)
#
#         logger.debug("path_ = %s" % path_)
#         logger.debug("file_ = %s" % file_)
#
#         return static_file(file_, path_)
#     else:
#         logger.debug("Error: File don't exist on server.")
#         return "Error: File don't exist on server."


@app.route('/resource/<filename>')
def route_resource(filename):
    """
    Get the files inside template directory
    :param path:
    :return:
    """
    #filename = path

    this_dir_ = this_dir()
    path =  os.path.join(this_dir_, 'resource/')
    logger.warn("ROUTE: /resource = %s" % filename)
    logger.warn("_path = %s" % path)

    return static_file(filename, path)



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

    table = []

    for tag in tags:
        tagid, tagname = tag
        url = "".join(["/tagid/", str(tagid)])
        link = link_tpl(url, tagname)

        _tags = zotero.get_related_tags(tagid)
        tags_links = [link_tpl("/tagid/%s" % tagid, tagname ) for tagid, tagname in _tags]
        related_tags = " ".join(tags_links)
        #related_tags = "   Related: %s<br />" % related_tags

        table.append([link, related_tags])
        #html = html + link + related_tags + "<br />\n"

    html = py2html.html_table(table=table)

    return template(base_template, subtitle="Tags", content=html, backlink="index")


@app.route('/tagid/<tagid:int>')
def route_tagid(tagid):
    logger.warn("ROUTE: /tagid = %s" % tagid)

    tagname = zotero.get_tagname(tagid)
    items = zotero.filter_tag(tagid)

    subtilte_ = "Tag: " + tagname

    tags = zotero.get_related_tags(tagid)
    tags_links = [link_tpl("/tagid/%s" % tagid, tagname ) for tagid, tagname in tags]
    item_tag_links = " ".join(tags_links)
    related_tags = "Related Tags: %s<br />" % item_tag_links


    html = related_tags + html_item_link_list(items)

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
    The ZOTSERVER - ZOTERO SERVER - Is a http web server that uses bottle framework. <br />
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


@app.route('/shutdown2server')
def route_shutdown():
    """
    Route to Kill Server Process
    :return:
    """
    import os
    ip=request.environ.get('REMOTE_ADDR')
    # the server can only be shutdown from localhost
    if ip == '127.0.0.1':
        os._exit(1)


@app.route('/coverid/<itemid:int>')
def route_coverid(itemid):

    picture = item_picture(itemid)

    print  "picture = %s" % picture

    if picture is None:
        return "Error picture not found"

    path, filename = os.path.split(picture)

    print "filename = %s" % filename
    print "path = %s" % path

    return static_file(filename, path)


@app.route("/settings")
def route_settings():
    """
    User settings route
    """

    return "settings"



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

    run(app=logged_app, host=HOST, port=PORT,  server=SERVER , debug=DEBUG, reloader=True)


# Run the server 
if __name__ == "__main__":
    main()
