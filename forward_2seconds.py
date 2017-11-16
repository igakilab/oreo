#このプログラムは2秒間前進し、その後停止するプログラムです。
import time
import easygopiogo3

pi = easygopigo3.EasyGoPiGo3()
pi.set_motor_limits(pi.MOTOR_LEFT+pi.MOTOR_RIGHT,1000)

ntime = time.time()+2 #2秒後の時間を計算
pi.set_motor_dps(pi.MOTOR_RIGHT,500) #右モーターの回転
pi.set_motor_dps(pi.MOTOR_LEFT,500)  #左モーターの回転
while 1:                            #2秒間何もしない
    if(time.time > ntime):
        break

pi.set_motor_dps(pi.MOTOR_LEFT,0)    #右モーターの停止
pi.set_motor_dps(pi.MOTOR_RIGHT,0)   #左モーターの停止

print('done')                      #終了を出力
