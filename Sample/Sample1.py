import Getch as gch
# Key control Sample


import easygopigo3
egpi = easygopigo3.EasyGoPiGo3()

egpi.set_speed(500) #0~1000 sitei
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
    w = getch()
