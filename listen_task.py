#!/usr/bin/env python
import redis
import time
import json
import os
import thread
import client_lib.cpu as cpu
import client_lib.cpu_info as cpu_info
import client_lib.flower_water as flower_water
import client_lib.photo as photo
import client_lib.video as video
import client_lib.temperature as temperature
import client_lib.common as common
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_listen_task.txt',
                    filemode='a')
                    
redis_host = common.get_config('redis_host')
redis_port = common.get_config('redis_port')
redis_password = common.get_config('redis_password')
r = redis.Redis(host=redis_host, port=redis_port, db=0, password=redis_password)

while True:
    a = r.rpop('home_task')
    if a is None:
        time.sleep(3)
    else:
        logging.info("listen_task start:" + a)
        try:
            jo = json.loads(a)
            if jo['type'] == "water_open":
                #os.system('python /home/pi/my_room/water/open.py')
                #thread.start_new_thread(do_task,("python /home/pi/my_room/water/open.py",))
                thread.start_new_thread(flower_water.server_task_open,())
            elif jo['type'] == "water_close":
                #os.system('python /home/pi/my_room/water/close.py')
                #thread.start_new_thread(do_task,("python /home/pi/my_room/water/close.py",))
                thread.start_new_thread(flower_water.close,())
            elif jo['type'] == "cpu_fs_open":
                #os.system('python /home/pi/my_room/cpu/open_fs.py')
                #thread.start_new_thread(do_task,("python /home/pi/my_room/cpu/open_fs.py",))
                thread.start_new_thread(cpu.fs_open,())
            elif jo['type'] == "cpu_fs_close":
                #os.system('python /home/pi/my_room/cpu/close_fs.py')
                #thread.start_new_thread(do_task,("python /home/pi/my_room/cpu/close_fs.py",))
                thread.start_new_thread(cpu.fs_close,())
            elif jo['type'] == "make_photo":
                #thread.start_new_thread(do_task,("python /home/pi/my_room/photo/make_photo.py",))
                thread.start_new_thread(photo.upload,())
            elif jo['type'] == "take_video":
                #thread.start_new_thread(do_task,("python /home/pi/my_room/video/take_video.py",))
                thread.start_new_thread(video.upload,())
            elif jo['type'] == "get_temp":
                thread.start_new_thread(temperature.upload,())
            elif jo['type'] == "get_info":
                thread.start_new_thread(temperature.upload,())
                thread.start_new_thread(cpu_info.upload,())
                thread.start_new_thread(photo.upload,())
            else:
                print jo 
            time.sleep(1)
        except Exception,e:
            print e
            logging.info("listen_task error:" + e)
