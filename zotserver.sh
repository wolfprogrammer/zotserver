#!/bin/bash
#
#
ZOTSERVER_HOME="$HOME/zoterotool2"


# Get the current script path
_script="$(readlink -f ${BASH_SOURCE[0]})"

# Get the current script directory
_base="$(dirname $_script)"


#echo $_script
#echo $_base


cd $ZOTSERVER_HOME

STARTCMD="python  zotserver.py"
LOGFILE="/tmp/zotserver.log" 
PIDFILE="/tmp/zotserver.pid"

start() {
 echo "Starting Python Zotero Server on port 8080"

	nohup $STARTCMD  2>&1 > $LOGFILE &
	echo $! > $PIDFILE

}
stop() {
	echo "Stopping Zotero Server"
	kill  `cat $PIDFILE`	
	echo "Stopped .."  >  $LOGFILE

}
status() {
 	echo "Status of Zotero Server"
	tail -f $LOGFILE

}


case "$1" in
 start)
 start
 ;;
 stop)
 stop
 ;;
 status)
 status
 ;;
 *)
 echo "Python Zotero Server Daemon"       
 echo "Usage: track_ip_service {start|stop|status}"
 exit 1
 esac
exit 0 


