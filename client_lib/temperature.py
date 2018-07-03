#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import urllib
import common
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_temperature_info.txt',
                    filemode='a')
def get_info():
    channel =16 
    data = []
    j = 0

    GPIO.setmode(GPIO.BCM)

    time.sleep(1)

    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(channel, GPIO.HIGH)
    GPIO.setup(channel, GPIO.IN)

    while GPIO.input(channel) == GPIO.LOW:
      continue
    while GPIO.input(channel) == GPIO.HIGH:
      continue

    while j < 40:
      k = 0
      while GPIO.input(channel) == GPIO.LOW:
        continue
      while GPIO.input(channel) == GPIO.HIGH:
        k += 1
        if k > 100:
          break
      if k < 8:
        data.append(0)
      else:
        data.append(1)

      j += 1

    #print "sensor is working."
    #print data

    humidity_bit = data[0:8]
    humidity_point_bit = data[8:16]
    temperature_bit = data[16:24]
    temperature_point_bit = data[24:32]
    check_bit = data[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0

    for i in range(8):
      humidity += humidity_bit[i] * 2 ** (7-i)
      humidity_point += humidity_point_bit[i] * 2 ** (7-i)
      temperature += temperature_bit[i] * 2 ** (7-i)
      temperature_point += temperature_point_bit[i] * 2 ** (7-i)
      check += check_bit[i] * 2 ** (7-i)

    tmp = humidity + humidity_point + temperature + temperature_point
    is_wrong = False
    if check == tmp:
      print "temperature :", temperature, "*C, humidity :", humidity, "%"
    else:
      is_wrong = True
      print "wrong"
      print "temperature :", temperature, "*C, humidity :", humidity, "% check :", check, ", tmp :", tmp
    GPIO.cleanup()
    return temperature,humidity,is_wrong
                    

def upload():
    try:
        room_info = get_info()
        temperature = room_info[0]
        humidity = room_info[1]
        is_wrong = room_info[2]
        #if is_wrong is True:
        if temperature > 50:
            raise Exception("wrong temperature and humidity:"+str(temperature)+"----"+str(humidity))
        #return temperature,humidity
        config_api_url = common.get_config('api_url')
        api_url = config_api_url + "/upload?type=temperature&temperature=%.2f&humidity=%.2f" % (float(temperature),float(humidity))
        result = urllib.urlopen(api_url)
        logging.info('UPLOAD temperature and  humidity INFO:'+api_url)
        print "UPLOAD temperature and  humidity INFO SUCCESS!"
    except Exception as e:
        logging.info(e)
        print "cat not got temperature and humidity,upload data error!"
    
