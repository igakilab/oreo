#-*- coding:utf-8 -*-
import socket
host = "XXX.XXX.XXX.XXX"
port = 7777

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
try:
    while True:
        response = client.recv(1024)
        print "response = " + response
        print
        response = client.recv(4096)
except KeyboardInterrupt:
    print "done"
