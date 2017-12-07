import time
import Getch as gch
import picamera

# Keyboard shutter


getch = gch.Getch()
w = getch()
while w!='e':
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.start_preview()
        time.sleep(2)
        camera.capture('cap.jpg')
        print("capture")
    w=getch()
