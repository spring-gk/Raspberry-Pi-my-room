#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
import time  
import thread
import logging
import requests
import json
import common
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_cpu_fs.txt',
                    filemode='a')

GPIO_PIN = 21
GPIO.setwarnings(False)

def fs_open():
    print "cpu_fs open"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN,GPIO.LOW)
    #time.sleep(60)
    #GPIO.cleanup()
    logging.info("cpu_fs open")

def fs_close():
    print "cpu_fs close"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN,GPIO.HIGH)
    #time.sleep(1)
    GPIO.cleanup()
    logging.info("cpu_fs close")

def auto_check():
    try:
        logging.info("auto check cpu_fs switch start!")
        file = open("/sys/class/thermal/thermal_zone0/temp")
        temp = float(file.read()) / 1000
        file.close()
        print "cpu temperature : %.1f" %temp
        logging.info("cpu_fs check,temperature : %.1f" %temp)
        #client auto task to check that wheather open the water switch
        config_api_url = common.get_config("api_url")
        #get the config info from server
        api_url = config_api_url + "/data?type=config"
        result = requests.get(url=api_url)
        if result.status_code == 200:
            result_text = result.text
            logging.info("config info:" + result_text)
            config_info = json.loads(result_text)
            print config_info
            config_cpu_temperature = config_info['data']['cpu_temperature']
            #check 
            if temp > config_cpu_temperature:
                return fs_open()
            else:
                return fs_close()
        else:
            raise Exception("can not get config info from the server!")
    except Exception as e:
        print "can not get config info from the server!"
        logging.info(e)