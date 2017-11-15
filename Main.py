import subprocess
import os
import math
import atexit
import threading
import sys
import Sub
IMG_DIR = "/var/www/html/photo/" #生成されるファイルのディレクトリ

#ゲーム開始
def main():
    print("main called")

    #ゲーム開始時に採点画像を削除
    index = 1
    while True:
        path = IMG_DIR+"saiten/cap"+str(index)+".png"
        if(os.path.exists(path)):
            os.remove(path)
            index+=1
        else:
            break
    # 採点結果のテキストファイルを初期化
    f = open("/var/www/html/photo/saiten/kekka.txt", "w")
    f.write("0,0,")
    f.close()

    Sub.setControl(True) #コントロール可能に
    print("main end")

#ゲーム終了
def stop():
    print("stop start")

    Sub.setControl(False)  #コントロール不能に
    print("communicate")
    import time
    time.sleep(1) #終了時に撮影していた時のために採点が終了するまで待っているつもり
    client.send("0\n")
    
    print("stop end")


if __name__ =="__main__":
    import socket
    host = "192.168.12.147" #javaプログラムが動いているPCのIPアドレス
    port = 50001 #ポート
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IPv4,TCPソケット作成
    client.connect((host,port)) #接続
    flg = False #ゲームの起動と終了が交互に実行されるようにフラグを設定
                # False = 起動待ち True = 終了待ち
    Sub.sub() #Sub起動
    while (True):
        ms = client.recv(2).rstrip() #2byte受信後(recv)　右側の空白を削除(rstrip)
        if(ms == "0" and not flg): #受信したメッセージが'0'で起動待ち状態なら
            flg=not flg #終了待ち状態に変更
            print("start Main")
            main() #起動
            client.send("0\n") #起動したことをPC側に送信
        elif(ms=="1" and flg): #受信したメッセージが'1'で終了待ち状態なら
            flg= not flg #起動待ち状態に変更
            print("stop Main")
            stop() #停止
