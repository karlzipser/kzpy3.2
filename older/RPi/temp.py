"""
ssh pi@192.168.43.20


Karls-MacBook-Pro:~ karlzipser$
nc -l -p 8080 | mplayer -fps 20 -demuxer h264es -


raspivid -t 10000 -w 300 -h 300 -fps 20 -o - | nc 192.168.43.243 8081
nc -l -p 8081 | mplayer -fps 20 -demuxer h264es - -dumpstream -dumpfile ~/Desktop/stream4.avi


pi@raspberrypi:~$
raspivid -t 100000 -w 300 -h 300 -fps 20 -o - | nc 192.168.43.243 8080


nc -l -p 8080 tee mplayer -fps 20 -demuxer h264es -
nc -l -p 8080 | tee mplayer -dumpstream -dumpfile ~/Desktop/stream4.avi | mplayer -fps 20 -demuxer h264es -
nc -l -p 8080 | tee mplayer -fps 20 -demuxer h264es - | mplayer -dumpstream -dumpfile ~/Desktop/stream4.avi





nc -l -p 8080 | mplayer -fps 60 -cache 1024 -



mplayer -vo png -fps 20  stream4.avi




##################
to view and save:
raspivid -t 100000 -w 640 -h 480 -fps 30 -o - | nc 192.168.43.243 8080

nc -l -p 8080 | tee mplayer -dumpstream -dumpfile ~/Desktop/stream4.avi | mplayer -fps 60 -demuxer h264es -

to view saved:
mplayer -fps 30 ~/Desktop/stream4.avi

to convert to png files:
mplayer -vo png -fps 30  ~/Desktop/temp/stream4.avi
#################


ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py; reset

ssh pi@192.168.43.20
sudo python kzpy3/scratch/camera_control.py
sudo python kzpy3/scratch/command_listener.py
"""


"""
sudo ipython
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)
pwm_motor = GPIO.PWM(40,50)
pwm_motor.start(0)
f = 50
pwm_motor.ChangeFrequency(f);pwm_motor.ChangeDutyCycle(7.2);time.sleep(0.3);pwm_motor.ChangeDutyCycle(0)

ds = 7.8
fs = [50,70,50,60,50,70,50] #[70,50,70,50,60,50,70,50,60]
for f in fs:
    print f
    pwm_motor.ChangeFrequency(f);pwm_motor.ChangeDutyCycle(ds);time.sleep(0.3);pwm_motor.ChangeDutyCycle(0);time.sleep(0.3)


for f in fs:
    if f == 50:
        ds = 7.2
    else:
        ds = 7.8
    print f;pwm_motor.ChangeFrequency(f);pwm_motor.ChangeDutyCycle(ds);time.sleep(0.3);pwm_motor.ChangeDutyCycle(0);time.sleep(1)


def motor_reverse(pwm_motor):
    for f in [70,50]:
        pwm_motor.ChangeFrequency(f);pwm_motor.ChangeDutyCycle(7.8);time.sleep(0.2)
    pwm_motor.ChangeDutyCycle(0)



"""




import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import RPi.GPIO as GPIO

import paramiko
hup = txt_file_to_list_of_strings('/home/pi/pw_MacbookPro.txt') 
host = hup[0]
port = 22
transport = paramiko.Transport((host, port))
password = hup[2]
username = hup[1]
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

distal_command_file_path = '/Users/karlzipser/scratch/2015/11/RPi_images/executed_commands'
local_command_file_path = '/home/pi/Desktop/executed_commands/command.txt'

SERVO_IN = 38
MOTOR_IN = 40

out_pins = [SERVO_IN,MOTOR_IN]

def gpio_setup():
    print('gpio_setup')
    GPIO.setmode(GPIO.BOARD)
    for p in out_pins:
        GPIO.setup(p,GPIO.OUT)



def do_pwm(pwm,duration,duty_cycle):
    start_time = time.time()
    pwm.ChangeDutyCycle(duty_cycle)
    while time.time() < start_time + duration:
        pass;
    pwm.ChangeDutyCycle(0)




###############
last_cmd ='no command yet'
servo_pwm_state = 9.5
servo_pwm_right_max = 11
servo_pwm_left_min = 7.2
servo_pwm_center = 9.5

command_file_path = '/home/pi/Desktop/distal_command.txt'

def update():
    global last_cmd
    global servo_pwm_state
    global servo_pwm_right_max
    global servo_pwm_left_min
    try:
        cmd_lst = txt_file_to_list_of_strings(command_file_path)    
        if cmd_lst[0] != last_cmd:
            last_cmd = cmd_lst[0]
            #print(last_cmd)
            if last_cmd[0] == ' ':
                """
                
                for i in range(5):
                    print('pwm_motor')
                    start_time = time.time()
                    pwm_motor.start(7.2)
                    while time.time() < start_time + 0.3:
                        pass;
                    pwm_motor.stop()
                    time.sleep(1.0)
                """

                print('motor')
                do_pwm(pwm_motor,0.3,7.20)

                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s('motor',t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))

            if last_cmd[0] == 'c':
                print('GPIO.cleanup(), gpio_setup()')
                GPIO.cleanup()
                gpio_setup()
                
            if last_cmd[0] == 'o':
                print('L')
                servo_pwm_state -= (servo_pwm_right_max-servo_pwm_left_min)/10.0
                if servo_pwm_state < servo_pwm_left_min:
                    servo_pwm_state = servo_pwm_left_min
                print(servo_pwm_state)
                do_pwm(pwm_servo,0.3,servo_pwm_state)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s(servo_pwm_state,t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))
                
            if last_cmd[0] == 'p':
                print('R')
                servo_pwm_state += (servo_pwm_right_max-servo_pwm_left_min)/10.0
                if servo_pwm_state > servo_pwm_right_max:
                    servo_pwm_state = servo_pwm_right_max
                print(servo_pwm_state)
                do_pwm(pwm_servo,0.3,servo_pwm_state)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s(servo_pwm_state,t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))
                
            elif str_contains(last_cmd,'up'):
                print('straight')
                servo_pwm_state = servo_pwm_center
                do_pwm(pwm_servo,0.3,servo_pwm_state)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s(servo_pwm_state,t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))
                
            elif str_contains(last_cmd,'left'):
                print('left')
                servo_pwm_state = servo_pwm_left_min
                do_pwm(pwm_servo,0.3,servo_pwm_state)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s(servo_pwm_state,t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))
                
            elif str_contains(last_cmd,'right'):
                print('right')
                servo_pwm_state = servo_pwm_right_max
                do_pwm(pwm_servo,0.3,servo_pwm_state)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s(servo_pwm_state,t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))
                
            elif last_cmd[0] == 'q':
                #list_of_strings_to_txt_file(command_file_path,['done.'])
                print('Quitting now. Press ctrl-C if this does not exit.')
                pwm_motor.stop()
                pwm_servo.stop()
                GPIO.cleanup()
                sys.exit()
    except KeyboardInterrupt:
        print('Quitting now.')
        GPIO.cleanup()
        sys.exit(1)
    except Exception,e:
        print str(e)
    time.sleep(0.01)


gpio_setup() 
pwm_motor = GPIO.PWM(40,50)
pwm_servo = GPIO.PWM(38,50)
pwm_motor.start(0)
pwm_servo.start(0)

print('\n*** command_listener.py: start this after keypress_view_RPi.py ***')
while True:
	update()
#########