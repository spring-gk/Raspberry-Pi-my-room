#!/usr/bin/env python
import os
import time
import requests
import common 

def upload():
    #take video
    name = str(int(time.time()))
    #filename = os.path.join(os.path.abspath("tmp"),name)
    tmp = os.path.join(os.path.dirname(__file__), "tmp")
    filename = os.path.join(tmp,name)

    os.system("raspivid -o %s.h264 -t 10000 -w 1280 -h 720"%(filename))
    os.system("MP4Box -fps 30 -add %s.h264 %s.mp4"%(filename,filename))

    #upload the video to server
    api_url = common.get_config('api_url')
    url = api_url + "/upload"
    data = {
        'type': 'video'
    }
    files = {'file': open(filename+".mp4", 'rb')}
    response = requests.post(url, data=data, files=files)
    print response.content

    #delete tmp files
    os.system("rm -rf %s.h264"%(filename))
    os.system("rm -rf %s.mp4"%(filename))
