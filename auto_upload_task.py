#!/usr/bin/env python
import client_lib.cpu_info as cpu_info
import client_lib.temperature as temperature
import logging
import thread
import time 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_auto_upload_task.txt',
                    filemode='a')
                    
if __name__ == '__main__':
    while True:
        logging.info("auto_upload_task start")
        #upload cpu info
        cpu_info.upload()
        #thread.start_new_thread(cpu_info.upload,())
        #upload temperature and humidity
        temperature.upload()
        #thread.start_new_thread(temperature.upload,())
        logging.info("auto_upload_task end")
        time.sleep(5)
