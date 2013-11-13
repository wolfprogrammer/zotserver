#!/bin/bash
#
#  This script controls the zotero-server as a daemon.
#
#  ZOTSERVER_HOME = Directory whre is the "zoteroserver.py"
#
#
#ZOTSERVER_HOME="$HOME/zoterotool2"
ZOTSERVER_HOME="$PWD"                # Current directory

# Get the current script path
_script="$(readlink -f ${BASH_SOURCE[0]})"

# Get the current script directory
_base="$(dirname $_script)"

BROWSER=firefox

#echo $_script
#echo $_base




cd $ZOTSERVER_HOME

STARTCMD="python  zotserver.py"
LOGFILE="/tmp/zotserver.log" 
PIDFILE="/tmp/zotserver.pid"
#exit 0

start() {
 echo "Starting Python Zotero Server on port 8080"

	nohup $STARTCMD  2>&1 > $LOGFILE &
	echo $! > $PIDFILE
	$BROWSER localhost:8080

}
stopp() {
	echo "Stopping Zotero Server"
	kill  `cat $PIDFILE`	
	echo "Stopped .."  >  $LOGFILE

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
 echo "Python Zotero Server Daemon"       
 echo "Usage: track_ip_service {start|stop|status|reload}"
 exit 1
 esac
exit 0 


