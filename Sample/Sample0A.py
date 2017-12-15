import time
import easygopigo3
pi = easygopigo3.EasyGoPiGo3()
pi.set_motor_limits(pi.MOTOR_LEFT+pi.MOTOR_RIGHT,1000)

ntime = time.time()+2
pi.set_motor_dps(pi.MOTOR_RIGHT,500)
pi.set_motor_dps(pi.MOTOR_LEFT,500)
while 1:
    if(time.time()>ntime):
        break

    
pi.set_motor_dps(pi.MOTOR_RIGHT,0)
pi.set_motor_dps(pi.MOTOR_LEFT,0)
print('done')
