import time
import Getch as gch
import picamera

# Keyboard shutter


getch = gch.Getch()
w = getch()
while w!='e':
    with picamera.PiCamera() as camera: #picamera使用
        camera.resolution = (1024,768) #カメラの解像度設定
        camera.start_preview() #準備開始
        time.sleep(2) #準備待ち
        camera.capture('cap.jpg') #撮影
        print("capture")
    w=getch()
