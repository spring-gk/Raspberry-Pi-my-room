#!/bin/sh
nohup python /home/pi/my_room/auto_check_cpu_fs_task.py >> /home/pi/my_room/auto_check_cpu_fs_task.log &
nohup python /home/pi/my_room/auto_check_flower_water_task.py >> /home/pi/my_room/auto_check_flower_water_task.log &
nohup python /home/pi/my_room/auto_upload_task.py >> /home/pi/my_room/auto_upload_task.log &
nohup python /home/pi/my_room/listen_task.py >> /home/pi/my_room/listen_task.log &
