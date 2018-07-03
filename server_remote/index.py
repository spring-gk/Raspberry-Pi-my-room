#!/usr/bin/env python
import shutil
import os
import os.path
import logging
import pymysql
import time
import tornado.ioloop
import tornado.web
import json
import redis
import types
import tornado.httpserver
import tornado.options
import tornado.httpclient
import tornado.websocket
import urllib

MYSQL_HOST = '139.129.201.179'
MYSQL_PORT = 3306
MYSQL_USER = 'my_room'
MYSQL_PASSWD = '2y12EQTRvWTapmF0'
MYSQL_DB = 'my_room'
REDIS_HOST = '139.129.201.179'
REDIS_PORT = 6379
REDIS_PASSWD='1qaz2wsx'
LISTNAME='listname_'
LISTLEN = 200
ROOM_ID = 1

#设置日志记录格式
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='my_room.log',
                    filemode='a')
#拍照列表
class PhotoHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute("SELECT photo_url,FROM_UNIXTIME(created,'%Y-%m-%d %H:%i:%s') as upload_time FROM room_photo ORDER BY created DESC LIMIT 0,20")
        r = cur.fetchall()
        cur.close()
        conn.close()
        self.render('photo.html',photo=r)

#视频列表
class VideoHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute("SELECT video_url FROM room_video ORDER BY created DESC LIMIT 0,20")
        r = cur.fetchall()
        cur.close()
        conn.close()
        self.render('video.html',video=r)

#室内温度湿度信息列表
class TemperatureHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute("SELECT temperature,humidity,FROM_UNIXTIME(created,'%Y-%m-%d %H:%s:%s') as create_time FROM room_info ORDER BY created DESC LIMIT 0,20")
        r = cur.fetchall()
        cur.close()
        conn.close()
        self.render('temperature.html',temperature=r)
        
#前台首页及AJAX请求加入任务队列，PI端执行队列任务
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write('main')
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        
        cur.execute("SELECT * from cpu_info ORDER BY id DESC LIMIT 1")
        cpu_info = cur.fetchone()
        
        cur.execute("SELECT * from room_info ORDER BY id DESC LIMIT 1")
        room_info = cur.fetchone()
        
        cur.execute("SELECT cpu_temperature,temperature,humidity,FROM_UNIXTIME(updated,'%Y') as update_year,FROM_UNIXTIME(updated,'%m') as update_month,FROM_UNIXTIME(updated,'%d') as update_day from room_config ORDER BY id DESC LIMIT 1")
        room_config = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        data = {
            'cpu_info':"",
            'room_info':'',
            'room_config':'',
            'tip_info':''
        }
        data['cpu_info'] = cpu_info
        data['room_info'] = room_info
        data['room_config'] = room_config
        if room_info['temperature'] <= room_config['temperature']:
            data['tip_info'] = "主人，偶已经是饱饱的啦，不需要浇水啦~"
        else:
            data['tip_info'] = "主人，好渴啊，快给我浇浇水啦~"
        self.render('index.html',info=data)
    
    def do_action(self,type,data=""):
        data = '{"type":"%s","data":"%s"}'%(type,data)
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWD)
        r.lpush('home_task',data)
        return True
    
    def post(self):
        response_body = {
            'code':"500",
            'msg':'',
            'data':'',
        }
        type = self.get_argument('type',"")
        logging.info('Do Job:'+type)
        #response_body['msg'] = type;
        try:
            if type == "water_open":
                res = self.do_action(type,"")
                if res is True:
                    response_body['code'] = 200
                    response_body['msg'] = 'water open successd !'
                else:
                    response_body['msg'] = 'water open failed !'
            elif type == "water_close":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'water close successd !'
                else:
                   response_body['msg'] = 'water close failed !'
            elif type == "get_info":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'get info successd !'
                else:
                   response_body['msg'] = 'get info failed !'
            elif type == "get_temp":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'get temp successd !'
                else:
                   response_body['msg'] = 'get temp failed !'
            elif type == "make_photo":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'make photo successd !'
                else:
                   response_body['msg'] = 'make photo failed !'
            elif type == "take_video":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'take video successd !'
                else:
                   response_body['msg'] = 'take video failed !'
            elif type == "cpu_fs_open":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'cpu fs open successd !'
                else:
                   response_body['msg'] = 'cpu fs open failed !'
            elif type == "cpu_fs_close":
                res = self.do_action(type,"")
                if res is True:
                   response_body['code'] = 200
                   response_body['msg'] = 'cpu fs close successd !'
                else:
                   response_body['msg'] = 'cpu fs close failed !'
            elif type == "flower_water_finish":
               message = {"flower_water_finish":1} 
               #推送到websocket
               SocketHandler.send_to_all({'type':"flower_water_finish",'message':message})
               response_body['code'] = 200
               response_body['msg'] = 'flower_water_finish successd !'
            else:
                response_body["msg"] = "error request!";
        except Exception as e:
            #response_body['msg'] = e
            response_body['msg'] = "异常错误"
        self.write(response_body)

#上传系统信息、室内温度湿度信息、拍照和视频上传
class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        response_body = {
            'code':"500",
            'msg':'',
            'data':'',
        }
        type = self.get_argument('type',"")
        now_time = int(time.time())
        try:
            if type == "":
               raise Exception("upload error")
            if type == "cpu_info":
                temperature = self.get_argument("temperature", "0.00")
                cpu_use = self.get_argument("cpu_use", "0.00")
                ram_used = self.get_argument("ram_used", "0.00")
                ram_free = self.get_argument("ram_free", "0.00")
                disk_used = self.get_argument("disk_used", "not goted")
                disk_perc = self.get_argument("disk_perc", "not goted")
                sql = "INSERT INTO `cpu_info`(`temperature`,`created`,`cpu_use`,`ram_used`,`ram_free`,`disk_used`,`disk_perc`) VALUES (%0.2f,%d,%.2f,%.2f,%.2f,'%s','%s')" % (float(temperature),now_time,float(cpu_use),float(ram_used),float(ram_free),disk_used,disk_perc)
                message = {"temperature":temperature,"cpu_use":cpu_use,"ram_used":round(float(ram_used)/1024,2)*100,"ram_free":ram_free,"disk_used":disk_used,"disk_perc":disk_perc}
                
            elif type == "temperature":
                temperature = self.get_argument("temperature", "0.00")
                humidity = self.get_argument("humidity", "0.00")
                if (float(temperature) < 100 and float(humidity) < 100) :
                    sql = "INSERT INTO `room_info`(`temperature`,`humidity`,`created`) VALUES (%0.2f,%0.2f,%d)" % (float(temperature),float(humidity),now_time)
                    # 实时数据进入redis
                    pushToRedis('temperature', json.dumps({"time":now_time, "data":float(temperature)}), float(temperature))
                    pushToRedis('humidity', json.dumps({"time":now_time,"data":float(humidity)}), float(humidity))
                    message = {"temperature":temperature,"humidity":humidity}
                else :
                    sql=''
            else:
                raise Exception("upload error")

            if (sql!=''):
                conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()
                #推送到websocket
                SocketHandler.send_to_all({'type':type,'message':message})
                
                logging.info('GET INFO:'+sql)
            response_body['code'] = 200
            response_body['msg'] = "upload data success!"
        except Exception as e:
            #response_body['msg'] = e
            logging.info(e)
            response_body['msg'] = "error happend!"
        self.write(response_body)
        
    def post(self):
        type = self.get_argument('type', '')
        if type == "":
           self.wrtie("Upload error")
           exit(0)
        upload_path=os.path.join(os.path.dirname(__file__),'uploadfiles')
        file_metas=self.request.files['file']  
        for meta in file_metas:
            filename=meta['filename']
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:    
                up.write(meta['body'])
        #insert into db
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
        cur = conn.cursor()
        now_time = int(time.time())
        if type == "photo":
            file_url = "/uploadfiles/"+filename
            sql = "INSERT INTO `room_photo`(`photo_url`,`created`) VALUES ('%s',%d)" % (file_url,now_time)
        else:
            file_url = "/uploadfiles/"+filename
            sql = "INSERT INTO `room_video`(`video_url`,`created`) VALUES ('%s',%d)" % (file_url,now_time)
        cur.execute(sql)
        conn.commit()
        conn.close()
        #推送到websocket
        upload_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        message = {"file_url":file_url,'upload_time':upload_time}
        SocketHandler.send_to_all({'type':type,'message':message})
        
        logging.info('GET INFO:'+sql)
        self.write('Upload %s finished!'%(type))

#获取配置信息
class DataHandler(tornado.web.RequestHandler):
    def get(self):
        response_body = {
            'code':"500",
            'msg':'',
            'data':'',
        }
        type = self.get_argument('type',"")
        try:
            if type == "":
                raise Exception("参数错误！")
            elif type == "config":
                #客户端获取配置信息
                conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                cur.execute("SELECT * from room_config WHERE id=1")
                config_info = cur.fetchone()
                conn.commit()
                cur.close()
                conn.close()
                
                response_body['code'] = 200
                response_body['data'] = config_info
            elif type == "info":
                #首页AJAX获取系统信息和室内信息
                conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                
                cur.execute("SELECT * from cpu_info ORDER BY id DESC LIMIT 1")
                cpu_info = cur.fetchone()
                
                cur.execute("SELECT * from room_info ORDER BY id DESC LIMIT 1")
                room_info = cur.fetchone()
                
                conn.commit()
                cur.close()
                conn.close()
                
                data = {
                    'cpu_info':"",
                    'room_info':''
                }
                data['cpu_info'] = cpu_info
                data['room_info'] = room_info
                
                response_body['code'] = 200
                response_body['data'] = data
            else:
                raise Exception("参数错误！")
                
        except Exception as e:
            response_body['msg'] = "异常错误"
            response_body['e'] = e
        self.write(response_body)

#websocket 处理
class SocketHandler(tornado.websocket.WebSocketHandler):
    """docstring for SocketHandler"""
    clients = set()
    def check_origin(self, origin):
        #parsed_origin = urllib.parse.urlparse(origin)
        #return parsed_origin.netloc.endswith(".xin.com")
        return True

    @staticmethod
    def send_to_all(message):
        if isinstance(message,dict):
            message_str = json.dumps(message)
        else:
            message_str = message
        print(message_str)
        for c in SocketHandler.clients:
            c.write_message(message_str)

    def open(self):
        self.write_message(json.dumps({
            'type': 'sys',
            'message': 'Welcome to MyRoom WebSocket'
        }))
        SocketHandler.send_to_all({
            'type': 'sys',
            'message': str(id(self)) + ' has joined'
        })
        SocketHandler.clients.add(self)

    def on_close(self):
        SocketHandler.clients.remove(self)

    def on_message(self, message):
        #SocketHandler.send_to_all({
        #    'type': 'comment',
        #    'message': message,
        #    'cid':self.get_argument('cid')
        #})
        pass
        
        
# 配置阀值参数
class ConfigSetHandler(tornado.web.RequestHandler):
    def post(self):
        response_body = {
            'code': "500",
            'msg': '',
            'data': '',
        }
        cpu_temperature = self.get_argument('cpu_temperature', 0.00)
        temperature = self.get_argument('temperature', 0.00)
        humidity = self.get_argument('humidity', 0.00)
        dictvalue = {"cpu_temperature":cpu_temperature, "temperature":temperature, "humidity":humidity}
        dictvalue['updated'] = time.time()

        try:
            if len(dictvalue) == 0:
                raise Exception("参数不能为空！")
            else:
                # 客户端获取配置信息
                conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB)
                cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
                for key in dictvalue.keys():
                    if (float(dictvalue[key]) > 0):
                        sql = 'update `room_config` set '
                        sql = sql+' `'+key+'` = %f '+" WHERE id=%d"
                        cur.execute(sql % (float(dictvalue[key]), 1))
                config_info = cur.fetchone()
                conn.commit()
                cur.close()
                conn.close()

                response_body['code'] = 200
                response_body['data'] = config_info

        except Exception as e:
            response_body['msg'] = "保存失败"
            # logging.info(e)

        self.write(response_body)

# 设置不同类型的温度到redis中
def pushToRedis(type, svalue, tmp):
    if type == "":
        raise Exception("参数不能为空！")
    else:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWD)
        listname = LISTNAME+'_'+type
        listlen = r.llen(listname)
        if (listlen < LISTLEN):
            r.lpush(listname,svalue)
        else:
            r.rpop(listname)
            r.lpush(listname,svalue)

    if (type == "temperature"):
        SocketHandler.send_to_all({'type': "redistemperature", 'message': {'data':tmp}})

    if (type == "humidity"):
        SocketHandler.send_to_all({'type': "redishumidity", 'message': {'data':tmp}})


class getInfoFromRedisHandler(tornado.web.RequestHandler):
    def post(self):
        response_body = {
            'code': "500",
            'msg': '',
            'data': '',
        }
        type = self.get_argument('type', "")

        try:
            if type == "":
                raise Exception("参数不能为空！")
            else:
                newlist=gettmpfromredis(type)

                response_body['code'] = 200
                response_body['msg'] = 'success'
                response_body['data'] = newlist

        except Exception as e:
            response_body['code'] = 500
            response_body['e'] = e
            response_body['msg'] = "异常错误"
        self.write(response_body)

def gettmpfromredis(type):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWD)
    listname = LISTNAME + '_' + type
    listlen = r.llen(listname)
    newlist = []
    if (listlen):
        list = r.lrange(listname, 0, LISTLEN)
        nowlistlen = len(list)
        n = 0
        while n < nowlistlen:
            newlist.append(json.loads(list[n].decode('utf8')))
            n = n + 1
    return newlist

if __name__ == "__main__":
    app = tornado.web.Application(
    handlers=[
      (r"/", IndexHandler), 
      (r"/upload", UploadHandler),
      (r"/data", DataHandler),
      (r"/updconf", ConfigSetHandler),
      (r"/gettmp", getInfoFromRedisHandler),
      (r"/photo", PhotoHandler),
      (r"/video", VideoHandler),
      (r"/temperature", TemperatureHandler),
      (r"/live", SocketHandler),
    ],
    debug = True,
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    uploadfiles_path = os.path.join(os.path.dirname(__file__), "uploadfiles")
    )
    app.listen(2404)
    tornado.ioloop.IOLoop.instance().start()
