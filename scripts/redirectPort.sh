#!/bin/bash
#----------------------------------------------------------------------#
#  Note: This script only works on Linux                               #
#  Note: This script must be run as root.                              #
#----------------------------------------------------------------------#
#   Redirect port 80 to port 8080                                      #
# This allows the zotserver.sh daemon run as non root in port 80.      #
# And allows the script be executed from localhost or from outside.    #
#                                                                      #
#  To test this script: Open in the browser. http://localhost          #
#                                                                      #
#----------------------------------------------------------------------#

SRC_PORT=8080   # Non-privileged port which the server is listening.
DST_PORT=80     # Http port which the server cannot run
IFACE=wlan3     # Network Interface

iptables -A INPUT -i $IFACE -p tcp --dport $DST_PORT -j ACCEPT
iptables -A INPUT -i $IFACE -p tcp --dport $SRC_PORT -j ACCEPT
iptables -A PREROUTING -t nat -i $IFACE -p tcp --dport $DST_PORT -j REDIRECT --to-port $SRC_PORT

    
#(Redirect from localhost) redirect 80 port to 8080 (port which the server is listening)
iptables -t nat -A OUTPUT -d localhost -p tcp --dport $DST_PORT -j REDIRECT --to-port $SRC_PORT

