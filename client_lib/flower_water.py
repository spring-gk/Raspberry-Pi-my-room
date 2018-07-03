#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import common
import logging
import requests
import json
import temperature

WATER_GPIO_PIN = 20
GPIO.setwarnings(False)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_flower_water.txt',
                    filemode='a')
def server_task_open():
    print "flower_water open"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WATER_GPIO_PIN, GPIO.OUT)
    GPIO.output(WATER_GPIO_PIN,GPIO.LOW)
    time.sleep(10)
    GPIO.cleanup()
    config_api_url = common.get_config("api_url")
    api_url = config_api_url + "/"
    result = requests.post(api_url,data={'type': 'flower_water_finish'})
    print(result.text)
    logging.info("flower_water switch opend!")
                    
def open():
    print "flower_water open"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WATER_GPIO_PIN, GPIO.OUT)
    GPIO.output(WATER_GPIO_PIN,GPIO.LOW)
    #time.sleep(5)
    #GPIO.cleanup()
    logging.info("flower_water switch opend!")

def close():
    print "flower_water close"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WATER_GPIO_PIN, GPIO.OUT)
    GPIO.output(WATER_GPIO_PIN,GPIO.HIGH)
    #time.sleep(1)
    GPIO.cleanup()
    logging.info("flower_water switch closed!")

def auto_check():
    try:
        logging.info("auto check water switch start!")
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
            config_temperature = config_info['data']['temperature']
            config_humidity = config_info['data']['humidity']
            #check 
            room_info = temperature.get_info()
            room_temperature = room_info[0]
            room_humidity = room_info[1]
            is_wrong = room_info[2]
            #if room_temperature > config_temperature and is_wrong == False:
            if room_temperature > config_temperature and room_temperature < 50:
                return open()
            if room_humidity < config_humidity:
                return open()
            return close()
        else:
            raise Exception("can not get config info from the server!")
    except Exception as e:
        print "can not get config info from the server!"
        logging.info(e)
