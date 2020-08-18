#!/bin/sh
DIR_NAME="/data/$(date +%F-%H%M)";
FILE_NAME="$(date +%H-%M-%S)"
if [ ! -d "$DIR_NAME" ]; then mkdir "$DIR_NAME"; fi

if [ ! -d "$DIR_NAME/arp" ]; then mkdir "$DIR_NAME/arp"; fi
watch -n 15 'arp -vn | tee --append $DIR_NAME/arp/$FILE_NAME' &>/dev/null &

if [ ! -d "$DIR_NAME/route" ]; then mkdir "$DIR_NAME/route"; fi
watch -n 15 'route -n | tee --append $DIR_NAME/route/$FILE_NAME' &>/dev/null &

if [ ! -d "$DIR_NAME/pcaps" ]; then mkdir "$DIR_NAME/pcaps"; fi
tcpdump -ne -w $DIR_NAME/pcaps/randcrawler.pcap -C 100 &

python3 randcrawler.py