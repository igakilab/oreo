import numpy as np
import cv2
import Getch as gch
import picamera
import io
import time

#キーボード入力で写真を撮影、採点後保存

#採点し保存する関数
#frameは画像が入ったnumpy配列
def saitenAndOutput(frame):
    flag =False #マーカーが範囲内に存在したかどうか
    if(frame is None): return #画像が存在しなければ戻る
    monitorSize= np.array(frame.shape[0:2]) #画像の大きさ取得 戻り値は[縦、横]

    targetUpperLeft = monitorSize / 6 *1 #採点範囲の左上設定
    targetDownRight = monitorSize / 6 *5 #採点範囲の右下設定

    targetUpperLeft = (targetUpperLeft[1] ,targetUpperLeft[0]) #[横、縦]に変換

    targetDownRight = (targetDownRight[1] ,targetDownRight[0])

    frame = cv2.GaussianBlur(frame, (5, 5), 0) #ガウシアンぼかし　エッジを抽出しやくする


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV画像に変換
    h = hsv[:, :, 0] #色
    s = hsv[:, :, 1] #彩度
    v = hsv[:, :, 2] #明度
    mask = np.zeros(h.shape, dtype=np.uint8) #元画像と同じ領域を確保
    mask[((h < 5) | (h > 165)) & (s > 110) & (v > 90)] = 255 #赤色の部分のみ255(黒)に設定
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #白黒画像から輪郭を抽出


    rects = []
    for contour in contours: #見つけた輪郭について
        epsilon = 0.1 * cv2.arcLength(contour, True)
        app = cv2.approxPolyDP(contour ,epsilon ,True) #輪郭を直線で近似

        if(app.shape[0 ] == 4): #近似した輪郭の頂点が4つ=四角形
            area = cv2.contourArea(app) #見つけた輪郭で囲まれた面積を計算
            if (area > 5000): #領域が5000以上の大きさであれば
                ver = app[: ,0 ,:]
                print(ver)
                X = ver[: ,0] #X座標取り出し
                Y = ver[: ,1] #Y座標取り出し

                if(targetUpperLeft[0] < min(X)
                        and max(X ) <targetDownRight[0]
                        and targetUpperLeft[1] < min(Y)
                        and max(Y ) <targetDownRight[1]): #採点範囲内に四角形が含まれていたら
                    flag =True
                print(targetUpperLeft[0] < min(X)
                      and max(X ) <targetDownRight[0]
                      and targetUpperLeft[1] < min(Y)
                      and max(Y ) <targetDownRight[1])

                cv2.polylines(frame, [app], True, (255, 0, 0), 3) #見つけた四角形を描画


    cv2.rectangle(frame ,(targetUpperLeft[0] ,targetUpperLeft[1]
                         ) ,(targetDownRight[0] ,targetDownRight[1]) ,(0 ,255 ,0) ,50) #採点範囲描画

    cv2.imwrite("capture.jpg", frame)

getch = gch.Getch()
w = getch()
while w!='e' :
    with picamera.PiCamera() as camera: #カメラ使用
        camera.resolution = (1024, 768) #解像度設定
        camera.start_preview() #準備開始
        time.sleep(2)
        imgStream = io.BytesIO() #一時保存領域作成


        camera.capture(imgStream, format='jpeg') #jpeg画像として撮影、保存

        data = np.fromstring(imgStream.getvalue(), dtype=np.uint8) #numpy配列に変換
        image = cv2.imdecode(data, 1) #保存領域から画像を取得
        saitenAndOutput(image) #採点、保存
        w=getch()
