#!/bin/sh
ARP_DIR="/data/arp"
RT_DIR="/data/routes"
CAP_DIR="/data/pcaps"

if [ ! -d "$ARP_DIR" ]; then mkdir -p "$ARP_DIR"; fi
if [ ! -d "$RT_DIR/route" ]; then mkdir -p "$RT_DIR"; fi
if [ ! -d "$CAP_DIR" ]; then mkdir -p "$CAP_DIR"; fi
crontab /etc/cron.d/monitor-cron
cron &
tcpdump -ne -w $CAP_DIR/$(hostname)_$(date +%H-%M-%S).pcap -C 100 &

python3 randcrawler.py