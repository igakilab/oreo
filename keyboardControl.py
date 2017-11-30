
import Getch as gch
import easygopigo3
#EasyGoPiGo3 インスタンス化
egpi = easygopigo3.EasyGoPiGo3()

egpi.set_speed(500) #0~1000指定
getch = gch.Getch() #一文字取得

w = getch()
while w!='e' :
    if (w=='w') :
        egpi.forward() #前進
    elif w=='s' :
        egpi.backward() #後進
    elif w=='d' :
        egpi.right()  #右回転
    elif w=='a' :
        egpi.left() #左回転
    elif w=='x': 
        egpi.stop() #止まる
    w = getch()
