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

import picamera
import os
from time import sleep
import select
import sys

shutter_numb = 0

IMG_DIR = '/var/www/html/photo/'  # 生成されるファイルのディレクトリ
saiten = 0  # 採点結果の合計
index = 1  # 撮影した写真のインデックス

isControl = False


# frameを採点して採点した写真と採点結果を書き込む
def scoreAndOutput(frame):
    flag = False  # 条件を満たすマーカーが見つかったかどうか
    if (frame is None): return

    img_size = np.array(frame.shape[0:2])  # 画像の大きさ　(height,width)

    targetUpperLeft = img_size / 6 * 1  # 採点範囲の左上座標
    targetDownRight = img_size / 6 * 5  # 採点範囲の右上座標

    targetUpperLeft = (targetUpperLeft[1], targetUpperLeft[0])  # (width,height)に入れ替え

    targetDownRight = (targetDownRight[1], targetDownRight[0])

    frame = cv2.GaussianBlur(frame, (5, 5), 0)  # ガウスぼかし

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR画像をHSV画像に変換
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    mask = np.zeros(h.shape, dtype=np.uint8)  # 画像と同じ大きさ,要素全て0の配列作成
    mask[((h < 5) | (h > 165)) & (s > 110) & (v > 90)] = 255  # 赤色の部分のみ255(黒)に
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 輪郭を抽出

    rects = []
    for contour in contours:  # 認識した輪郭のループ
        epsilon = 0.1 * cv2.arcLength(contour, True)  # 近似する輪郭と元の輪郭の最大距離
        app = cv2.approxPolyDP(contour, epsilon, True)  # 認識した輪郭を直線で近似
        if (app.shape[0] == 4):  # 輪郭の頂点が4つ
            area = cv2.contourArea(app)  # 輪郭の面積
            if (area > 5000):
                ver = app[:, 0, :]
                print(ver)
                X = ver[:, 0]  # 輪郭のX座標ベクトル
                Y = ver[:, 1]

                if (targetUpperLeft[0] < min(X)  # 輪郭が採点範囲内に存在しているか
                        and max(X) < targetDownRight[0]
                        and targetUpperLeft[1] < min(Y)
                        and max(Y) < targetDownRight[1]):
                    flag = True
                print(targetUpperLeft[0] < min(X)
                      and max(X) < targetDownRight[0]
                      and targetUpperLeft[1] < min(Y)
                      and max(Y) < targetDownRight[1])

                cv2.polylines(frame, [app], True, (255, 0, 0), 3)  # 認識した輪郭を青色(255,0,0)で書き込み

    global index, saiten
    cv2.rectangle(frame, (targetUpperLeft[0], targetUpperLeft[1]),
                  (targetDownRight[0], targetDownRight[1]), (0, 255, 0), 50)  # 採点範囲を緑色(0,255,0),太さ50で書き込み
    if (flag):
        saiten = saiten + 1  # 点数プラス
    print("###################")
    cv2.imwrite(IMG_DIR + "saiten/cap" + str(index) + ".png", frame)  # 画像書き込み
    index += 1
    f = open(IMG_DIR + "saiten/kekka.txt", "w")  # 結果テキスト書きこみ
    f.write(str(index - 1) + "," + str(saiten) + ",")
    f.close()


WIDTH = 320  # ストリーミングする映像の横幅
HEIGHT = 240  # ストリーミングする映像の高さ
FPS = 30  # ストリーミングする映像のfps


# カメラのストリーミングが始まるとロックされ、ループ中にリリース・ロックが行われる

# カメラの初期化
def piCamera():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FPS
    time.sleep(2)
    return camera


import numpy as np
import cv2

global camera


# カメラ撮影後 scoreAndOutputに画像を渡す
def capture():
    global end
    print("acquire")
    imgStream = io.BytesIO()

    camera.resolution = (1920, 1080)  # 画像の解像度指定

    camera.start_preview()  # カメラ準備

    camera.capture(imgStream, format='jpeg')  # 撮影

    data = np.fromstring(imgStream.getvalue(), dtype=np.uint8)  # numpyの配列に変換
    image = cv2.imdecode(data, 1)  # 画像データに変換
    scoreAndOutput(image)


# ストリーミングを開始する関数
def main():
    global camera
    camera = piCamera()



def getCurrentAngle(client):
    tyousei = 0
    response1 = client.recv(4096)  # レシーブは適当な2の累乗にします（大きすぎるとダメ）

    response2 = str(client.recv(1024))  # レシーブは適当な2の累乗にします（大きすぎるとダメ）

    split = response2.split(" ")
    radX = float(split[3])
    radY = float(split[4][:split[4].find('\\r')])
    print(radX," ; ",radY)
    rad = math.acos(radX)
    print(rad)
    if radY < 0:
        rad=2*math.pi-rad

    return rad+tyousei


# gopigoを操作する関数
def control():
    SPEED_MAX = 470  # 最大速度

    pygame.init()  # pygame初期化
    pygame.joystick.init()
    # pygame.display.init()

    import socket

    host = "localhost"  # お使いのサーバーのホスト名を入れます //-------------------------------------------------------------ここ変える
    port = 7777  # 適当なPORTを指定してあげます

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # オブジェクトの作成をします

    client.connect((host, port))  # これでサーバーに接続します

    joystick = pygame.joystick.Joystick(0)  # joystick取得
    # joystickで使っている関数は以下の通り
    # joystick.event.get , joystick.get_axis
    joystick.init()  # joystick 初期化
    pi = easygopigo3.EasyGoPiGo3()  # easygopigo初期化
    # easygopigoで使っている関数は以下の通り
    # .set_motor_limits , .set_motor_dps
    pi.set_motor_limits(pi.MOTOR_LEFT + pi.MOTOR_RIGHT, 1000)  # モーターリミット設定

    print(joystick.get_name())
    time_shutter = None  # 次の撮影可能時間
    global index, saiten, isControl
    while 1:
        
        try:
            if not isControl:
                continue

            e = pygame.event.get()  # 入力されているイベントを取得,joystick.get～を呼び出す前に必ずこのメソッドを呼び出す

            yAxis = -1 * joystick.get_axis(1)  # y軸方向には前が-1,後ろが1になっているので反転
            xAxis = joystick.get_axis(0)  # 左が1,右が-1
            # pygame.event.clear()
            # print("shutter"+str(shutte))

            # ----------------撮影系-------------------

            isButtonPressed = False
            for i in e:  # 取得したイベントの中にボタン押下があるか
                if i.type == pygame.JOYBUTTONDOWN:
                    isButtonPressed = True

            if time_shutter == None:  # 一秒経過しているか
                if isButtonPressed:  # ボタン押されていたら
                    pi.set_motor_dps(pi.MOTOR_RIGHT, 0)  # モーター停止
                    pi.set_motor_dps(pi.MOTOR_LEFT, 0)
                    t = threading.Thread(target=capture)  # 撮影スレッド作成
                    t.setDaemon(True)  # 親スレッドが終了したときに終了するように設定
                    t.start()  # スレッドスタート

                    time_shutter = time.time() + 2  # 現在の時刻から2秒後の時間を設定

            else:
                if time_shutter - time.time() <= 0:  # 現在時刻のほうが遅かったらNoneに設定
                    time_shutter = None

            ##----------操作系---------------

            slope = math.sqrt(xAxis ** 2 + yAxis ** 2)  # 入力した傾き計算
            angle = math.tan(yAxis / xAxis)

            angle = math.acos(xAxis)
            print(yAxis)
            if yAxis < 0:
                angle = 2 * math.pi - angle

            #  print("xAxis :"+str(xAxis))
            #  print(2*(-(xAxis-0.4)*(xAxis-1)))
            #

            currentAngle = getCurrentAngle(client)

            minTargetAngle = angle - math.pi / 30
            maxTargetAngle = angle + math.pi / 30
            if minTargetAngle < 0 or 2 * math.pi < maxTargetAngle:
                if minTargetAngle < 0:
                    minTargetAngle = 2 * math.pi + minTargetAngle
                if 2 * math.pi < maxTargetAngle:
                    maxTargetAngle - 2 * math.pi

                if minTargetAngle < currentAngle or currentAngle < maxTargetAngle:
                    print("go")
                else:
                    print("turn")
            else:
                if minTargetAngle < currentAngle and currentAngle < maxTargetAngle:
                    print("go")
                else:
                    print("mawaru")

            if slope > 1:  # 傾きの最大を1に
                slope = 1

            if -0.2 < yAxis and yAxis < 0.2 and (0.7 < xAxis or xAxis < -0.7):  # 入力が真横周辺の場合前の処理を続ける
                continue  # 真横に入力しているつもりでもyが正か負かで旋回方向が変わるため

            elif yAxis >= 0:  # 前に倒した場合
                if (xAxis > 0):  # 左に倒した場合
                    xAxis = xAxis - 0.3  # 入力値を0.3引く　入力値が微量でもモーターが敏感に反応してしまうため
                    if (xAxis < 0):
                        xAxis = 0

                if (xAxis < 0):  # 右に倒した場合　上と処理は同じ
                    xAxis = -xAxis
                    xAxis = xAxis - 0.3
                    if (xAxis < 0):
                        xAxis = 0
                    xAxis = -xAxis
                # xAxis = xAxis-2*( -(xAxis-0.4)*(xAxis-1))

                speed_left = slope * SPEED_MAX  # 傾きから速度を計算
                speed_right = slope * SPEED_MAX

                if (xAxis > 0):
                    speed_left = speed_left * (1 - xAxis)  # 左に傾いていたら左のモーターの速度を落とす
                elif (xAxis < 0):
                    speed_right = speed_right * (1 - (-xAxis))  # 左と同じ


            else:  # 後ろに倒した場合

                # xAxis=-xAxis
                # xAxis = xAxis-2*( -(xAxis-0.2)*(xAxis-1))

                speed_left = -slope * SPEED_MAX  # 速度設定
                speed_right = -slope * SPEED_MAX

                if (xAxis > 0):
                    speed_left = speed_left * (1 - xAxis)
                elif (xAxis < 0):
                    speed_right = speed_right * (1 - (-xAxis))

            # print(yAxis)
            pi.set_motor_dps(pi.MOTOR_RIGHT, speed_left)  # 速度をモーターに設定
            pi.set_motor_dps(pi.MOTOR_LEFT, speed_right)  # 実際にモーターの速度を設定している部分
            time.sleep(0.01)
        except KeyboardInterrupt:
            break;

    print("done")


# mainから呼び出される
# コントローラーで操作できるかを指定
def setControl(b):
    if b:  # 次のゲームが開始された(b=True)のとき撮影した写真のインデックスと点数を初期化
        global index, saiten
        index = 1
        saiten = 0
    global isControl
    isControl = b


# mainから最初に呼び出される
def sub():
    control_thread = threading.Thread(target=control)  # 操作用スレッド開始
    control_thread.setDaemon(True)  # 親スレッドが消えた時に自動で気に消えるように設定
    control_thread.start()

    main_thread = threading.Thread(target=main)  # ストリーミングスレッド開始
    main_thread.setDaemon(True)  # 親スレッドが消えた時に自動で気に消えるように設定
    main_thread.start()
