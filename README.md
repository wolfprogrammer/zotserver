# zotserver
=========

See Zotero:  http://www.zotero.org/

Zotserver is a standalone Zotero python web server, based on bottle framework that allows the user 
to share and search their files in his Zotero library from everywhere, Tablets, Smartphones or any Computer
in the network, PDAs ... Remote locations.

This software can be useful to share documents, technical standards, books,magazines, references through internet and local network or any kind of file.

## Features

1. Full text search in Zotero library
2. Search by Tags
3. Search by Collections
4. Access your Zotero's Library in any Browser from everywhere
   

## Description

````
The server uses the following files:
1. zotserver.py   -  Is the sever core application
2. zoterolib.py   -  A python library to read Zotero library metadata
3. zotserver.conf -  User configuration file. It will be copied to  $HOME/.zotserver.conf
4. zotdaemon.sh   -  Daemon launcher. To start/stop the server.
3. scripts/update.sh -  A bash script to get the Zotero Library data to storage directory
4. scripts/findprofiles.py  - Find zotero storage directory (on Unix)
````

In Linux the data can be found in:
~/.mozilla/firefox/<profile>/zotero/storage
~/.mozilla/firefox/<profile>/zotero/zotero.sqlite

In Windows it can be found in:
C:\Documents and Settings\<username>\Application Data\Mozilla\Firefox\Profiles\<randomstring>\zotero  

For more information see: http://www.zotero.org/support/zotero_data

## Dependencies

The server in production mode uses cherrypy.


## Install and Deployment

````bash
$ cd zotserver
$ cd scripts
$ ./findprofiles.py 
USERNAME =  tux
FIREFOX  =  /home/tux/.mozilla/firefox
{'mwad0hks.default': '/home/tux/.mozilla/firefox/mwad0hks.default/zotero'}

# edit update.sh and set it to: /home/tux/.mozilla/firefox/mwad0hks.default/zotero
# it will copy zotero dabase and data to target directory

# run 
cd cd zotserver
# edit zotdaemon.sh to point to the zotserver absolute path
./zotdaemon.sh start

# Open http://localhost:8080
````



### Local Setup

```  bash
      cd
      git clone  https://github.com/wolfprogrammer/zotserver.git
      cd zotserver
      # Find the firefox Profile directory where the Zotero's data is stored.
      # ~/.mozilla/firefox/<profile>/zotero/
      # edit the update-data.sh
      ./update-data.sh  # It will copy   zotero/storage and zotero/zotero.sqlite to the directory
                                         from this script is.
```
                                         
      
### Local Deployment

```  bash
     cd $HOME/zotserver
     ./zotdaemon.sh start
     The server will open on      
       *  http://localhost:8080                   : Accessing from local computer
       *  htpp://<server-ip or host name>:8080    : Accessing from somewhere
```                                  
     
### Remote Setup

The server can also be installed in a different machine from which Zotero is installed.
     
### Screenshots

![ScreenShot](https://github.com/wolfprogrammer/zotserver/blob/master/screenshots/screen1.png)

![ScreenShot](https://github.com/wolfprogrammer/zotserver/blob/master/screenshots/screen2.png)

![ScreenShot](https://github.com/wolfprogrammer/zotserver/blob/master/screenshots/screen3.png)
