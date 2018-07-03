#!/usr/bin/env python
import os
import requests
import common
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log_cpu_info.txt',
                    filemode='a')

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
# Return RAM information (unit=kb) in a list                                      
# Index 0: total RAM                                                              
# Index 1: used RAM                                                                
# Index 2: free RAM                                                                
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Return % of CPU used by user as a character string                               
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
 
# Return information about disk space as a list (unit included)                    
# Index 0: total disk space                                                        
# Index 1: used disk space                                                        
# Index 2: remaining disk space                                                    
# Index 3: percentage of disk used                                                 
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def upload():
    try:
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()
         
        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used = round(int(RAM_stats[1]) / 1000,1)
        RAM_free = round(int(RAM_stats[2]) / 1000,1)
         
        # Disk information
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        #DISK_perc = DISK_stats[3]
        DISK_perc = DISK_stats[2]
        config_api_url = common.get_config('api_url')
        api_url = config_api_url + "/upload?type=cpu_info&temperature=%.2f&cpu_use=%.2f&ram_used=%s&ram_free=%s&disk_used=%s&disk_perc=%s" % (float(CPU_temp),float(CPU_usage),str(RAM_used),str(RAM_free),str(DISK_used),str(DISK_perc))
        print api_url
        #os.system("curl "+api_url)
        result = requests.get(url=api_url)
        logging.info('UPLOAD CPU INFO:'+api_url)
        print "UPLOAD CPU INFO SUCCESS!"
    except Exception as e:
        print "UPLOAD CPU INFO SUCCESS failed!"
        logging.info(e)