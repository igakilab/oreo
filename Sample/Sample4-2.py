import numpy as np
import cv2
import Getch as gch
import picamera
import io
import time
def saitenAndOutput(frame):
    flag =False
    if(frame is None): return
    monitorSize= np.array(frame.shape[:3][0:2])

    targetUpperLeft = monitorSize / 6 *1
    targetDownRight = monitorSize / 6 *5

    targetUpperLeft = (targetUpperLeft[1] ,targetUpperLeft[0])

    targetDownRight = (targetDownRight[1] ,targetDownRight[0])

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
        app = cv2.approxPolyDP(contour ,epsilon ,True)
        if(app.shape[0 ] == 4):
            area = cv2.contourArea(app)
            if (area > 5000):
                ver = app[: ,0 ,:]
                print(ver)
                X = ver[: ,0]
                Y = ver[: ,1]

                if(targetUpperLeft[0] < min(X)
                        and max(X ) <targetDownRight[0]
                        and targetUpperLeft[1] < min(Y)
                        and max(Y ) <targetDownRight[1]):
                    flag =True
                print(targetUpperLeft[0] < min(X)
                      and max(X ) <targetDownRight[0]
                      and targetUpperLeft[1] < min(Y)
                      and max(Y ) <targetDownRight[1])

                cv2.polylines(frame, [app], True, (255, 0, 0), 3)


    cv2.rectangle(frame ,(targetUpperLeft[0] ,targetUpperLeft[1]
                         ) ,(targetDownRight[0] ,targetDownRight[1]) ,(0 ,255 ,0) ,50)

    global index
    cv2.imwrite("saiten"+str(index)+".jpg", frame)

index = 0
img = cv2.imread("cap"+str(index)+".jpg")
while not img is None:
    print("saiten cap"+str(index)+".jpg")
    saitenAndOutput(img)
    index=index+1
    img = cv2.imread("cap"+str(index)+".jpg")

print("end")