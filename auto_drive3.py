import socket
import time
import pygame
import easygopigo3
#モーターを駆動
def motor_on(speed):#speed = 回転速度
    pi.set_motor_dps(pi.MOTOR_RIGHT,speed-10)
    pi.set_motor_dps(pi.MOTOR_LEFT,speed)
#モーターを止める
def motor_off(): #引数なし
    pi.set_motor_dps(pi.MOTOR_RIGHT,0)
    pi.set_motor_dps(pi.MOTOR_LEFT,0)
    

SPEED = 300     #モーターの回転速度
CENTER = 246    #フィールドの中央座標
DISTANCE = 100  #相手との距離
host = "150.89.234.246" #socket通信を行う相手のIPアドレス
port = 7777     #socket通信に使用するPORT

pi = easygopigo3.EasyGoPiGo3()      #EasyGoPiGo3()の初期化

pi.set_motor_limits(pi.MOTOR_LEFT+pi.MOTOR_RIGHT,1000)      #モーターの回転速度の上限値の設定

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #socket通信の定型文
client.connect((host,port))                                 #socket通信の構築

opponent = None         #Playerの座標情報
last_opponent = None    #Playerの前回の座標情報
oneself = None          #自分の座標情報
last_oneself            #自分の前回の座標情報
ab = None               #Playerと自分の距離の絶対値
cnt = 0                 #Playerの座標情報を連続で受け取った回数
cnt2 = 0                #自分の座標情報を連続で受け取った回数

pi.set_motor_dps(pi.MOTOR_RIGHT,0)  #右モーターの回転速度の初期化
pi.set_motor_dps(pi.MOTOR_LEFT,0)   #左モーターの回転速度の初期化

try:
    while True :
        print("--------------------------")
        response = client.recv(4096)            #socketを受信
        print "response = "+response
        if response[0:1] != '=':               #受け取っとソケットが既定の文字列になっていなかったらcontinue
            continue
        slice = response[2:3]                   #responseの2文字目を抜き取る
        if slice == '1':                       #socketがPlayerの座標なら
            last_opponent = opponent            
            print "opponent "+response
            opponent = int(response.split(' ')[3].split('.')[0])    #座標情報を抜き出し整数型にキャスト
            cnt+=1                                                   
            cnt2=0
            print "cnt = "+str(cnt) 
        elif slice == '2' :                   #socketが自分の座標なら
            last_oneself = oneself
            print "oneself  "+response
            oneself = int(response.split(' ')[3].split('.')[0])     #座標情報を抜き出し整数型にキャスト
            cnt = 0
            cnt2+=1
        else :                                #どちらでもなかったら
            print ("motor stop")
            motor_off()                        #モーターを止める
        if cnt > 6 :                           #Playerの座標情報を連続で6回以上受け取ったらエリアの外に出たと判断
             print ("out area")
             outtime = time.time()+2            #2秒後の時間を記録
             if last_oneself<CENTER :           #前回の自分の座標が中央より左なら
                 while(time.time() <= outtime): #2秒間
                    print last_oneself
                    motor_on(-1*SPEED)          #後退
             else :
                 while(time.time() <= outtime):#中央より右なら
                     print last_oneself
                     motor_on(1*SPEED)          #前進
             cnt=0
             continue
        elif cnt >0:
             continue
        if cnt2 > 6 :
            motor_off()
        elif cnt > 0:
            continue

        if opponent == None or oneself == None: #どちらかの座標情報が取得できていないなら
            continue                           #continue
        else :                                  #違ったら
            print "opponent = " + str(opponent)
            print "oneself = "+ str(oneself)
            ab = abs(opponent-oneself)          #Playerと自分の距離の絶対値を計算
            print "abs = "+str(ab)
            
            if ab >=DISTANCE :#Playerと自分の距離が規定値より大きかったら
                print ("dont move")
                motor_off()   #モーターストップ
            elif  last_opponent !=None :#Playerの前回座標が取得できて入る
                if last_opponent - opponent >= 0:   #Playerが左に進んでいたら
                    print("move front")
                    motor_on(SPEED)     #前進
                else :                  #Playerが右に進んでいたら
                    print ("move back")
                    motor_on(-1*SPEED)   #後退
            else :
                continue
    
        response = client.recv(8192)    #詰まっているsocketを受信
except KeyboardInterrupt:
    motor_off()
    print
    print('done')

