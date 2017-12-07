import Getch as gch
# キーボードで操作する


import easygopigo3
egpi = easygopigo3.EasyGoPiGo3() #初期化

egpi.set_speed(500) #スピードを設定　0から1000まで指定可能
getch = gch.Getch()

w = getch() #一文字取得
while w!='e' : #'e'キーが入力されたら終了
    if (w=='w') :
        egpi.forward() #前に進む
    elif w=='s' :
        egpi.backward() #後ろに進む
    elif w=='d' :
        egpi.right() #右に進む
    elif w=='a' :
        egpi.left() #左に進む
    elif w=='x':
        egpi.stop() #止まる
    w = getch()
