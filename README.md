# zotserver
=========

See Zotero:  http://www.zotero.org/

Zotserver is a standalone Zotero python web server, based on bottle framework that allows the user 
to share and search their files in his Zotero library from everywhere, Tablets, Smartphones or any Computer
in the network, PDAs ... Remote locations.

This software can be useful to share couments, technical standards, references through internet, local network
or any kind of file.

Features:
   1. Full text search in Zotero library
   2. Search by Tags
   3. Search by Collections
   4. Access your Zotero's Library in any Browser from everywhere
   

The server uses the following files:
  1. zotserver.py   -  Is the sever core application
  2. zoterotool.pu  -  A tool to search the Ztero library
  3. update-data.sh -  A bash script to get the Zotero Library data 
                       In Linux:  ~/.mozilla/firefox/<profile>/zotero/storage
                                  ~/.mozilla/firefox/<profile>/zotero/zotero.sqlite
    
  4. update-data-remote.sh - A bash script to get the Zotero Library data through rsync from where
                             the Zotero is installed.
  5. zotserver.sh   - A bash script to deploy the server as a daemon.
                             

To the sever work only needs the Zotero data.  


## Install
There is only the need of python bottle framework and Zotero data.

Local Setup

      cd
      git clone  https://github.com/wolfprogrammer/zotserver.git
      cd zotserver
      # Find the firefox Profile directory where the Zotero's data is stored.
      # ~/.mozilla/firefox/<profile>/zotero/
      # edit the update-data.sh
      ./update-data.sh  # It will copy   zotero/storage and zotero/zotero.sqlite to the directory
                                         from this script is.
      
Local Deployment
     cd $HOME/zotserver
     ./zotserver.sh start
     The server will open on      
       *  http://localhost:8080                   : Accessing from local computer
       *  htpp://<server-ip or host name>:8080    : Accessing from somewhere
                                  
     
Remote Setup
     The server can also be installed in a different machine from which Zotero is installed.
     
     
     
