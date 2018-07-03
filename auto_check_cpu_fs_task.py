#!/usr/bin/env python
import client_lib.cpu as cpu
import logging
import thread
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_auto_check_task.txt',
                    filemode='a')
                    
if __name__ == '__main__':
    while True:
        logging.info("auto_check_task start")
        #auto_check cpu_fs swithch
        #cpu.auto_check()
        thread.start_new_thread(cpu.auto_check,())
        logging.info("auto_check_task end")
        time.sleep(30)
