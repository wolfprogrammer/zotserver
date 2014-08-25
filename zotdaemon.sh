#!/bin/bash
#
#  This script controls the zotero-server as a daemon.
#  requires curl
#
#  Debian/Ubuntu: apt-get install curl
#
#-------------------------------------------------------

#---------- S E T T I N G S ---------------------------#

# Absolute path to installation directory
ZOTSERVER_HOME=/home/tux/PycharmProjects/zotserver
PIDFILE="/tmp/zotserver.pid"
SERVERPORT=8080

#-----------------------------------------------------#

# Get the current script path
_script="$(readlink -f ${BASH_SOURCE[0]})"
#echo "Script absolute path "$_script

# Get the current script directory
_base="$(dirname $_script)"
#echo "Script Directory "$_base

# Default directory
BROWSER=firefox

#
# Assume that the zotserver.py is in the
# same directory of this script
#
cd $ZOTSERVER_HOME
STARTCMD="python  zotserver.py"

#exit 0

start() {
 echo "Starting Python Zotero Server on port 8080"

	nohup $STARTCMD   2>&1 > /dev/null &
	#echo $! > $PIDFILE
	#cat $PIDFILE
	#$BROWSER localhost:8080

}
stopp() {
	echo "Stopping Zotero Server"
    curl 'http://127.0.0.1:'$SERVERPORT/shutdown2server 2>&1 > /dev/null
}
status() {
 	echo "Status of Zotero Server"
	tail -f $LOGFILE

}

reload() {
    echo "Reloading zotsever ..."
    stopp   
    sleep 5
    start

}

case "$1" in
 start)
 start
 ;;
 stop)
 stopp
 ;;
 status)
 status
 ;;
 reload)
 reload     
 ;;

 *)
 echo "Zotero Server Daemon"
 echo "Usage: $(basename $0) {start|stop|status|reload}"
 exit 1
 esac
exit 0 


