#!/usr/bin/python3
# -*- coding: utf-8 -*-

import zmq
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import threading
#import Serial_read.py

ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)
sub.setsockopt(zmq.SUBSCRIBE, b"")
sub.connect("tcp://192.168.1.36:5555")
#sub.setsockopt(zmq.SUBSCRIBE, b"")
#print(sub.setsockopt(zmq.SUBSCRIBE, b""))

#センサーデータ取得
def zmq_sub():
    while True:
        global json
        json = sub.recv_json()
        #print(json)

class Html(tornado.web.RequestHandler):

    def get(self):
        try:
            self.render(
                "test.html",
                time = json["Data"]["Timestamp"],
                value = json["Data"]["Current value"]
#                 a = [b"0",b"102",b"2"]
            )
#             self.write(json)
        except Exception as e:
            s = str(e)
            self.write(s.encode()
            )


def make_app():
    app = tornado.web.Application([(r"/", Html),])
if __name__ == '__main__':

    thread_data = threading.Thread(target=zmq_sub)
    thread_data.start()
    
    #ren_app = make_app()
    app = tornado.web.Application([(r"/", Html),])
#     thread_render = threading.Thread(target=make_app)
#     thread_render.start()
    

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8885)
    tornado.ioloop.IOLoop.instance().start()
    http_server.stop()