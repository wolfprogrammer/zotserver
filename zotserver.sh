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
LOCKFILE=/tmp/zotserver.lock

#
# Assume that the zotserver.py is in the
# same directory of this script
#
cd $ZOTSERVER_HOME
STARTCMD="python  zotserver.py"

#exit 0

start() {
 echo "Starting Python Zotero Server on port 8080"

	nohup $STARTCMD  >/dev/null 2>&1 &
	touch $LOCKFILE
	#echo $! > $PIDFILE
	#cat $PIDFILE
	#$BROWSER localhost:8080

}
stopp() {
	echo "Stopping Zotero Server"
    curl --silent 'http://127.0.0.1:'$SERVERPORT/shutdown2server >/dev/null 2>&1
    rm -rf $LOCKFILE
}
status() {

	if [ -e "$LOCKFILE" ]
    then
      echo "* Server Running"
    else
      echo "* Server Not Running"
    fi


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


