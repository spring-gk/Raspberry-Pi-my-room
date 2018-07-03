#!/bin/sh
source /root/MYROOM_ENV/bin/activate;cd /root/my_room/server_remote; nohup python index.py > server.log 2>&1 &
