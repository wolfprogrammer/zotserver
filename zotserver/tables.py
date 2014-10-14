#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, \
    ForeignKey, Index, Integer, LargeBinary, Numeric, Table, Text, text, \
    create_engine, ForeignKeyConstraint
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing.pickleable import Parent


Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    itemID = Column(Integer, primary_key=True)
    itemTypeID = Column(ForeignKey(u'itemTypes.itemTypeID'), nullable=False)
    dateAdded = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dateModified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    clientDateModified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    libraryID = Column()
    key = Column(Text, nullable=False)


# library = relationship(u'Library')
#    fulltextWords = relationship(u'FulltextWord', secondary='fulltextItemWords')
#    tags = relationship(u'Tag', secondary='itemTags')
#     parents = relationship(
#        u'Item',
#        secondary='itemSeeAlso',
#        primaryjoin=u'Item.itemID == itemSeeAlso.c.itemID',
#        secondaryjoin=u'Item.itemID == itemSeeAlso.c.linkedItemID'
#     )

class ItemAttachment(Base):
    __tablename__ = 'itemAttachments'

    item_id = Column(ForeignKey("items.itemID"), primary_key=True)

    sourceItemID = Column(ForeignKey("items.itemID"), index=True)
    linkMode = Column(Integer)
    mimeType = Column(Text, index=True)
    charsetID = Column(Integer)
    path = Column(Text)
    originalPath = Column(Text)
    syncState = Column(Integer, index=True, server_default=text("0"))
    storageModTime = Column(Integer)
    storageHash = Column(Text)

    #item = relationship("Item", backref=backref("itemAttachments", order_by=id))

    #itemID = relationship('Item', foreign_keys='itemAttachments.itemID')
    #sourceItemID = relationship('Item', foreign_keys='itemAttachments.sourceItemID')

    #Items = relationship("Item", backref=backref("itemAttachments", uselist=False))


    #__table_args__ = (ForeignKeyConstraint([itemID, sourceItemID], [Item.itemID, Item.itemID]), {})

    item = relationship(u'Item', primaryjoin='ItemAttachment.sourceItemID == Item.itemID')


class ItemDataValue(Base):
    __tablename__ = 'itemDataValues'

    valueID = Column(Integer, primary_key=True)
    value = Column(NullType)


class ItemDatum(Base):
    __tablename__ = 'itemData'

    itemID = Column(ForeignKey(u'items.itemID'), primary_key=True, nullable=False)
    fieldID = Column(ForeignKey(u'fields.fieldID'), primary_key=True, nullable=False, index=True)
    valueID = Column(ForeignKey(u'itemDataValues.valueID'))

    field = relationship(u'Field')
    item = relationship(u'Item')
    itemDataValue = relationship(u'ItemDataValue')


class ItemType(Base):
    __tablename__ = 'itemTypes'

    itemTypeID = Column(Integer, primary_key=True)
    typeName = Column(Text)
    templateItemTypeID = Column(Integer)
    display = Column(Integer, server_default=text("1"))


class FieldFormat(Base):
    __tablename__ = 'fieldFormats'

    fieldFormatID = Column(Integer, primary_key=True)
    regex = Column(Text)
    isInteger = Column(Integer)


class Field(Base):
    __tablename__ = 'fields'

    fieldID = Column(Integer, primary_key=True)
    fieldName = Column(Text)
    fieldFormatID = Column(ForeignKey(u'fieldFormats.fieldFormatID'))

    fieldFormat = relationship(u'FieldFormat')


class Collection(Base):
    __tablename__ = 'collections'

    collectionID = Column(Integer, primary_key=True)
    collectionName = Column(Text, nullable=False)
    parentCollectionID = Column(ForeignKey(u'collections.collectionID'), server_default=text("NULL"))
    dateAdded = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dateModified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    clientDateModified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    libraryID = Column(Integer)
    key = Column(Text, nullable=False)

    parent = relationship(u'Collection', remote_side=[collectionID])


engine = create_engine(r'sqlite:////home/tux/.zotserver/zotero.sqlite')
session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)


def print_tree(rows):
    def get_level_diff(row1, row2):
        """ Returns tuple: (from, to) of different item positions.  """
        if row1 is None:  # first row handling
            return (0, len(row2))
        assert len(row1) == len(row2)
        for col in range(len(row1)):
            if row1[col] != row2[col]:
                return (col, len(row2))
        assert False, "should not have duplicates"

    prev_row = None
    for row in rows:
        level = get_level_diff(prev_row, row)
        for l in range(*level):
            print 2 * l * " ", row[l]
            prev_row = row


# q = (
#     session.query(Item, ItemAttachment)
#     .filter_by(itemID=525)
#     .all())


# rows = (session.query(Item, ItemAttachment.itemID)
#         .join(ItemAttachment)
#         .filter(itemID=525).all()
#         )
#
# print rows

#print q


#print session.query(Item, ItemAttachment).all()

# print "-----------"
#
# print session.query(Collection.collectionName, Collection.collectionID).all()
#
# print "-----------"
#
#
#
# print "-----------"
#
# #session.query(Item, ItemAttachment).all()
#
#
# print session.query(ItemDatum, ItemDataValue , Field).all()
# #print session.query(Item.)