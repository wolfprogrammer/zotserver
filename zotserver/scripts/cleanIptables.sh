#!/bin/bash
#----------------------------------------------------------------------#
#
# Clean all Iptables firewall rules.
# Note: Must be run as root
#----------------------------------------------------------------------#
#
#

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT


echo "IPtables Rules Cleaned"
