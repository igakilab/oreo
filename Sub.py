import tornado.web
import tornado.websocket
import tornado.ioloop
import picamera
import io
import time
import threading
import pygame
import easygopigo3
import math

import subprocess
import picamera
import os
from time import sleep
import select
import sys

shutter_numb = 0

IMG_DIR = '/var/www/html/photo/'
saiten = 0
index = 1

isControl=False

saitenL = threading.Lock()
def saitenAndOutput(frame):
    flag=False
    if(frame is None): return
    monitorSize= np.array(frame.shape[:3][0:2])
        
    targetUpperLeft = monitorSize/6*1
    targetDownRight = monitorSize/6*5

    targetUpperLeft = (targetUpperLeft[1],targetUpperLeft[0])

    targetDownRight = (targetDownRight[1],targetDownRight[0])

    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 5) | (h > 165)) & (s > 110) & (v > 90)] = 255
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    rects = []
    for contour in contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        app = cv2.approxPolyDP(contour,epsilon,True)
        if(app.shape[0]==4):
            area = cv2.contourArea(app)
            if (area > 5000):
                ver = app[:,0,:]
                print(ver)
                X = ver[:,0]
                Y = ver[:,1]
                
                if(targetUpperLeft[0] < min(X)
                   and max(X)<targetDownRight[0]
                   and targetUpperLeft[1] < min(Y)
                   and max(Y)<targetDownRight[1]):
                    flag=True
                print(targetUpperLeft[0] < min(X)
                   and max(X)<targetDownRight[0]
                   and targetUpperLeft[1] < min(Y)
                   and max(Y)<targetDownRight[1])
                
                cv2.polylines(frame, [app], True, (255, 0, 0), 3)



    global index,saiten
    cv2.rectangle(frame,(targetUpperLeft[0],targetUpperLeft[1]
                                        ),(targetDownRight[0],targetDownRight[1]),(0,255,0),50)
    if (flag):
        saiten=saiten+1
    print("###################")
    cv2.imwrite(IMG_DIR+"saiten/cap"+str(index)+".png", frame)
    index+=1
    f=open(IMG_DIR+"saiten/kekka.txt","w")
    f.write(str(index-1)+","+str(saiten)+",")
    f.close()





WIDTH = 320
HEIGHT = 240
FPS = 30
wait = threading.Lock()

class HttpHandler(tornado.web.RequestHandler):
    def initialize(self):
            pass

    def get(self):
        print("ok")
        self.render("./index.html")  

class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, camera):
        print("init")
        self.camera = camera
        self.state = True

    def open(self):
        print(self.request.remote_ip, ": connection opened")
        #t = threading.Thread(target=self.loop)    
        #t.setDaemon(True)
        #t.start()
        from tornado.ioloop import PeriodicCallback
        self.stream = io.BytesIO()
        self.callback = PeriodicCallback(self.call,0.1)
        self.callback.start()
        
        
    def call(self):
        global wait
        count=0
        if not wait.acquire(False) :
            #print("wait")
            return
        camera.resolution = (WIDTH, HEIGHT)
        for f in self.camera.capture_continuous(self.stream, "jpeg", use_video_port=True):
            self.stream.seek(0)
            #print("send")
            buff = self.stream.read()
            self.write_message(buff,binary=True)
            self.stream.seek(0)
            self.stream.truncate()
            if not self.state:
                break
            wait.release()
            time.sleep(0.00001)
            count=count+1
            
            if count > 100:
                break
            if not wait.acquire(False):
                break

    def on_close(self):
        self.state = False     
        self.close()     
        print(self.request.remote_ip, ": connection closed")

def piCamera():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FPS
    time.sleep(2)        
    return camera

import numpy as np
import cv2

global camera
def capture():
    global end,waitbool,wait
    print("acquire")
    imgStream=io.BytesIO()
    #waitbool=True
    #end = False
    #while waitbool : continue
    wait.acquire()
    
    camera.resolution = (1920, 1080)

    camera.start_preview()
   
    camera.capture(imgStream,format='jpeg')
    #end = True
    wait.release()
    
    data = np.fromstring(imgStream.getvalue(),dtype=np.uint8)
    image = cv2.imdecode(data,1)
    saitenAndOutput(image)
        
def main():
    global camera
    camera = piCamera()
    print("complete initialization--------------------------------------------")
    app = tornado.web.Application([
        (r"/", HttpHandler),                     
        (r"/camera", WSHandler, dict(camera=camera)),   
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    print("listen")
    tornado.ioloop.IOLoop.instance().start()
    

def control():
    SPEED_MAX = 470  #

    turn_small = 0.4
    turn_large = 0.6

    speed_right = 0
    speed_left = 0
    pygame.init()
    pygame.joystick.init()
    pygame.display.init()
    
    joystick = pygame.joystick.Joystick(0)
    from pygame.locals import *
    joystick.init()
    pi = easygopigo3.EasyGoPiGo3()
    pi.set_motor_limits(pi.MOTOR_LEFT + pi.MOTOR_RIGHT, 1000)
    print(joystick.get_name())
    time_shut = None
    flg = True
    oldCap = False
    global index,saiten,isControl,wait
    while 1:

        try:
            
            if not isControl:
            	#pi.stop()
                print("isControl")
                oldCap = True
                #time.sleep(0.5)
            	

            if oldCap:
                global saitenL
                print("index init")
                oldCap = False
                wait.acquire()
                wait.release()
               
                
            e = pygame.event.get()

            yAxis = -1 * joystick.get_axis(1)
            xAxis = joystick.get_axis(0)
            pygame.event.clear()
            # print("shutter"+str(shutte))
            flag = False
            for i in e:
                if i.type == JOYBUTTONDOWN:
                    flag = True

            if time_shut == None:
                if flag:
                    pi.set_motor_dps(pi.MOTOR_RIGHT, 0)
                    pi.set_motor_dps(pi.MOTOR_LEFT, 0)
                    t = threading.Thread(target=capture)
                    t.setDaemon(True)
                    t.start()
                    #capture()
                    #cameraLoad()
                    #shutter()
                    #cameraSave()
                    time_shut = time.time() + 2
                    shutte = 0
            else:
                ##print("hoge"+str(time_shut-time.time()))
                if time_shut - time.time() <= 0:
                    time_shut = None

            angle = math.sqrt(xAxis ** 2 + yAxis ** 2)
            #  print("xAxis :"+str(xAxis))
            #  print(2*(-(xAxis-0.4)*(xAxis-1)))
            #
            if angle > 1:
                angle = 1

            if -0.2 < yAxis and yAxis < 0.2 and (0.7 < xAxis or xAxis < -0.7):
                continue



            elif yAxis >= 0:
                if (xAxis > 0):
                    xAxis = xAxis - 0.3
                    if (xAxis < 0):
                        xAxis = 0

                if (xAxis < 0):
                    xAxis = -xAxis
                    xAxis = xAxis - 0.3
                    if (xAxis < 0):
                        xAxis = 0
                    xAxis = -xAxis
                # xAxis = xAxis-2*( -(xAxis-0.4)*(xAxis-1))

                speed_left = angle * SPEED_MAX
                speed_right = angle * SPEED_MAX
                if (xAxis > 0):
                    speed_left = speed_left * (1 - xAxis)
                elif (xAxis < 0):
                    speed_right = speed_right * (1 - (-xAxis))


            else:
                # xAxis=-xAxis
                # xAxis = xAxis-2*( -(xAxis-0.2)*(xAxis-1))

                speed_left = -angle * SPEED_MAX
                speed_right = -angle * SPEED_MAX

                if (xAxis > 0):
                    speed_left = speed_left * (1 - xAxis)
                elif (xAxis < 0):
                    speed_right = speed_right * (1 - (-xAxis))

            #print(yAxis)
            pi.set_motor_dps(pi.MOTOR_RIGHT, speed_left)
            pi.set_motor_dps(pi.MOTOR_LEFT, speed_right)
            time.sleep(0.01)
        except KeyboardInterrupt:
            break;

    print("done")

def setControl(b):
    if b :
        global index,saiten
        index=1
        saiten=0
    global isControl
    isControl = b

def sub():
    
    
    x =threading.Thread(target=control)
    x.setDaemon(True)
    x.start()

    y =threading.Thread(target=main)
    y.setDaemon(True)
    y.start()
