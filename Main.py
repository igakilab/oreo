import subprocess
import os
import math
import atexit
import threading
import sys
import Sub
IMG_DIR = "/var/www/html/photo/"

def main():
    print("main called")
    index = 1
    while True:
        path = IMG_DIR+"saiten/cap"+str(index)+".png"
        if(os.path.exists(path)):
            os.remove(path)
            index+=1
        else:
            break
   
    Sub.setControl(True)
    print("main end")

    
def stop():
    print("stop start")

    Sub.setControl(False)
    print("communicate")
    import time
    time.sleep(1)
    client.send("0\n")
    
    print("stop end")
   
if __name__ =="__main__":
    import socket
    host = "192.168.12.147"
    port = 50001
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    flg = False
    Sub.sub()
    while (True):
        ms = client.recv(2).rstrip()
        print(ms)
        print(ms == "0")
        #print(controlProcess.communicate())
        if(ms == "0" and not flg):
            flg=not flg
            f = open("/var/www/html/photo/saiten/kekka.txt","w")
            f.write("0,0,")
            f.close()
            print("start Main")
            main()
            client.send("0\n")
        elif(ms=="1" and flg):
            flg= not flg
            print("stop Main")
            stop()
            #import easygopigo3
            
    
        
