#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tables import *
from pprint import pprint

def show_all_collections():
    q1 = session.query(Collection).all()
    print "\n\n"
    print "collectionID\tparentCollectionID\tcollectionName"
    for q in q1:
        print q.collectionID,"\t",q.parentCollectionID,"\t",  q.collectionName


def show_collection(collection_id):
    """
    Show collection given its id
    :param collection_id: Collection ID Number
    :type collection_id: int
    :return:
    """
    #q = session.query(Collection.collectionName, Collection.collectionID)
    q = session.query(Collection)
    qq = q.filter_by(collectionID=collection_id).one().__dict__.copy()
    return qq
    #import IPython ;  IPython.embed()





def filter_collection(collection):
     print session.query(Collection.collectionName, Collection.collectionID).\
         filter_by(collectionName=collection).all()

#=============== COMMAND LINE PARSER =======================#

import argparse
import sys

desc = "Interactive Database Test"
parser = argparse.ArgumentParser(prog='mathpy', description=desc)

parser.add_argument("--all-collections", action="store_true",  help="Show all collections")
parser.add_argument("--filter-collection", help="Filter collection")
parser.add_argument("--collection", help="<collection id> Show collection given its ID")
parser.add_argument("--compile-bin",action="store_true", help="Compile to binary object.")

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()

if args.all_collections:
    show_all_collections()

if args.filter_collection:
    filter_collection(args.filter_collection)

if args.collection:
    pprint(show_collection(int(args.collection)))

# elif args.uninstall:
#     p.uninstall()
# elif args.compile_bin:
#     p.compile_bin()
#
