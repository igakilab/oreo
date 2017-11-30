#shutterとkeyboardControlを組み合わせたもの
import cv2
index=0 #撮影した写真のインデックス
#採点メソッド#frameを採点して採点した写真と採点結果を書き込む
def scoreAndOutput(frame):
    flag=False #条件を満たすマーカーが見つかったかどうか
    if(frame is None): return


    img_size= np.array(frame.shape[0:2]) #画像の大きさ　(height,width)
        
    targetUpperLeft = img_size/6*1 #採点範囲の左上座標
    targetDownRight = img_size/6*5 #採点範囲の右上座標

    targetUpperLeft = (targetUpperLeft[1],targetUpperLeft[0]) #(width,height)に入れ替え

    targetDownRight = (targetDownRight[1],targetDownRight[0])

    frame = cv2.GaussianBlur(frame, (5, 5), 0) #ガウスぼかし

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #BGR画像をHSV画像に変換
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = np.zeros(h.shape, dtype=np.uint8) #画像と同じ大きさ,要素全て0の配列作成
    mask[((h < 5) | (h > 165)) & (s > 110) & (v > 90)] = 255 #赤色の部分のみ255(黒)に
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #輪郭を抽出


    rects = []
    for contour in contours: #認識した輪郭のループ
        epsilon = 0.1 * cv2.arcLength(contour, True) #近似する輪郭と元の輪郭の最大距離
        app = cv2.approxPolyDP(contour,epsilon,True) #認識した輪郭を直線で近似
        if(app.shape[0]==4): #輪郭の頂点が4つ
            area = cv2.contourArea(app) #輪郭の面積
            if (area > 5000):
                ver = app[:,0,:]
                print(ver)
                X = ver[:,0] #輪郭のX座標ベクトル
                Y = ver[:,1]
                
                if(targetUpperLeft[0] < min(X) #輪郭が採点範囲内に存在しているか
                   and max(X)<targetDownRight[0]
                   and targetUpperLeft[1] < min(Y)
                   and max(Y)<targetDownRight[1]):
                    flag=True
                print(targetUpperLeft[0] < min(X)
                   and max(X)<targetDownRight[0]
                   and targetUpperLeft[1] < min(Y)
                   and max(Y)<targetDownRight[1])
                
                cv2.polylines(frame, [app], True, (255, 0, 0), 3) #認識した輪郭を青色(255,0,0)で書き込み




    cv2.rectangle(frame,(targetUpperLeft[0],targetUpperLeft[1]
                                        ),(targetDownRight[0],targetDownRight[1]),(0,255,0),30) #採点枠書き込み
    global index
    

    print("###################")
    print(flag)
    cv2.imwrite("cap"+str(index)+".png", frame) #保存
    index+=1


        
import picamera
import io
import time
import numpy as np
def shutter():
     with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.start_preview()
        time.sleep(2)
        imgStream = io.BytesIO()
        camera.start_preview()
   
        camera.capture(imgStream,format='jpeg')

        data = np.fromstring(imgStream.getvalue(),dtype=np.uint8)
        image = cv2.imdecode(data,1)
        saitenAndOutput(image) #採点メソッドに投げる
    
import Getch as gch

import easygopigo3
egpi = easygopigo3.EasyGoPiGo3()

egpi.set_speed(500)
getch = gch.Getch()

w = getch()
while w!='e' :
    if (w=='w') :
        egpi.forward()
    elif w=='s' :
        egpi.backward()
    elif w=='d' :
        egpi.right()
    elif w=='a' :
        egpi.left()
    elif w=='x':
        egpi.stop()
    elif w=='c':
        shutter() #撮影
    w = getch()
    
