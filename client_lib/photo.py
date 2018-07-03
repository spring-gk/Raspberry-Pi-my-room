#!/usr/bin/env python
import os
import time
import requests
import common
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_photo.txt',
                    filemode='a')
def upload():
    try:
        #make photo
        name = str(int(time.time()))+".jpg"
        #filename = os.path.join(os.path.abspath("tmp"),name)
        tmp = os.path.join(os.path.dirname(__file__), "tmp")
        filename = os.path.join(tmp,name)
        os.system("raspistill -o %s -t 2000 -w 1024 -h 768"%(filename))

        #upload photo to the server
        api_url = common.get_config('api_url')
        url = api_url + "/upload"
        data = {
            'type': 'photo'
        }
        files = {'file': open(filename, 'rb')}
        response = requests.post(url, data=data, files=files)
        print response.content

        #delete tmp files
        os.system("rm -rf %s"%(filename))
        
        logging.info("upload photo:"+filename)
    except Exception as e:
        print "upload photo failed!"
        logging.info(e)
