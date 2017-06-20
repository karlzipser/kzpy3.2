"""

ipython --pylab osx kzpy3/scratch/keypress_view_RPi.py; reset

ssh pi@192.168.43.20
sudo python kzpy3/scratch/camera_control.py
sudo python kzpy3/scratch/command_listener.py
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

def motor_reverse(pwm_motor):
    for f in [70,50]:
        pwm_motor.ChangeFrequency(f);pwm_motor.ChangeDutyCycle(7.8);time.sleep(0.2)
    pwm_motor.ChangeDutyCycle(0)



###############
last_cmd ='no command yet'
servo_pwm_state = 9.5
servo_pwm_right_max = 11
servo_pwm_left_min = 7.2
servo_pwm_center = 9.5
reverse_state = False
command_file_path = '/home/pi/Desktop/distal_command.txt'
last_cmd_time = time.time()

def update():
    global last_cmd
    global servo_pwm_state
    global servo_pwm_right_max
    global servo_pwm_left_min
    global reverse_state
    global last_cmd_time
    if time.time() - last_cmd_time > 1:
        pwm_motor.ChangeDutyCycle(0);
        pwm_servo.ChangeDutyCycle(0);
        #print('time.time() - last_cmd_time > 1')
    try:
        cmd_lst = txt_file_to_list_of_strings(command_file_path)    
        if cmd_lst[0] != last_cmd:
            last_cmd_time = time.time()
            last_cmd = cmd_lst[0]
            #print(last_cmd)
            if last_cmd[0] == 'g':
                reverse_state = False
                print('motor')
                #do_pwm(pwm_motor,0.3,7.20)
                pwm_motor.ChangeDutyCycle(7.20)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s('motor',t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))

            if last_cmd[0] == ' ':
                print('stop')
                if reverse_state == False:
                    f = 60
                    f2 = 50
                
                    pwm_motor.ChangeFrequency(f)
                    pwm_motor.ChangeDutyCycle(7.8)
                    time.sleep(0.3)
                    
                    pwm_motor.ChangeDutyCycle(0)
                    pwm_motor.ChangeFrequency(f2)

                else:
                    print('stop only for forward drive')
                #pwm_motor.ChangeDutyCycle(7.20)
                t = str(time.time())
                list_of_strings_to_txt_file(local_command_file_path,[d2s('motor',t)])
                sftp.put(local_command_file_path, opj(distal_command_file_path,t+'.txt'))

            if last_cmd[0] == 'b':

                print('back up')
                if not reverse_state:
                    motor_reverse(pwm_motor)
                    reverse_state = True
                pwm_motor.ChangeFrequency(60)
                pwm_motor.ChangeDutyCycle(7.8)
                time.sleep(0.05)
                pwm_motor.ChangeDutyCycle(0);
                time.sleep(0.3)
                pwm_motor.ChangeFrequency(50)
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
                print('Quitting now...')
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