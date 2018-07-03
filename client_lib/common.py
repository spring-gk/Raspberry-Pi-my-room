#!/usr/bin/env python
import json

def get_config(key):
    file_object = open('/home/pi/my_room/client_lib/config.txt')
    try:
         config_info = file_object.read()
    finally:
         file_object.close()
    config_info = json.loads(config_info)
    if config_info[key]:
        return config_info[key]
    else:
        return ""