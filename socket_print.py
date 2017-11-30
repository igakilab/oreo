#-*- coding:utf-8 -*-
import socket
host = "XXX.XXX.XXX.XXX" #VSを動作させるPCのIPアドレス
port = 7777                 #VSとの通信を行うポート番号

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #魔法の言葉
client.connect((host,port))                               #接続

try:
    while True:
        response = client.recv(1024) #socketを受信
        print "response = " + response #socketの内容を出力
        print
        response = client.recv(4096) #不要なsocketを破棄する
except KeyboardInterrupt:
    print "done"
