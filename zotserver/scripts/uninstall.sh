#!/bin/bash
#
# file: uninstall.sh
# description: Uninstall the package zotserver from system
#
PACKAGE=zotserver
PYTHON_VERSION=2.7
SCRIPTS=/etc/init.d/zotserver



SITE_PACKAGE=/usr/local/lib/python$PYTHON_VERSION/dist-packages

PACKAGE_DIR=$SITE_PACKAGE/$PACKAGE
PACAKE_EGG=$PACKAGE_DIR-*.egg-info

echo $PACKAGE_DIR
echo $PACAKE_EGG

rm -rf $SCRIPTS
rm -rf $PACKAGE_DIR
rm -rf $PACAKE_EGG


echo "PACKAGE UNINSTALLED"

#/usr/local/lib/python2.7/dist-packages/zotserver-1.5.egg-info