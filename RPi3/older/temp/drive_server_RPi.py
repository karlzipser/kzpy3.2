import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
print os.path.basename(sys.argv[0])

import RPi.GPIO as GPIO

STEER_PIN = 35
MOTOR_PIN = 37
EYE_PIN = 31
NEUTRAL = 7.0
GPIO_TRIGGER_RIGHT = 13
GPIO_ECHO_RIGHT = 15
GPIO_TRIGGER_LEFT = 19
GPIO_ECHO_LEFT = 21
GPIO_REED = 23

out_pins = [STEER_PIN,MOTOR_PIN,EYE_PIN]
def gpio_setup():
    print('gpio_setup')
    GPIO.setmode(GPIO.BOARD)
    for p in out_pins:
        GPIO.setup(p,GPIO.OUT)

gpio_setup() 
pwm_motor = GPIO.PWM(MOTOR_PIN,50)
pwm_steer = GPIO.PWM(STEER_PIN,50)
pwm_motor.start(NEUTRAL)
pwm_steer.start(0)

GPIO.setup(GPIO_TRIGGER_RIGHT,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_RIGHT,GPIO.IN)      # Echo
GPIO.setup(GPIO_TRIGGER_LEFT,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO_LEFT,GPIO.IN)      # Echo

GPIO.setup(GPIO_REED, GPIO.IN, pull_up_down=GPIO.PUD_UP)

reed_close = 0
rps = 0

def my_callback(channel):
    global reed_close
    if GPIO.input(GPIO_REED): 
        pass #print "Rising edge detected"  
    else:
        #print "Falling edge detected" 
        reed_close += 1

GPIO.add_event_detect(GPIO_REED, GPIO.BOTH, callback=my_callback)
#
##############



##############
#
import socket
#import select
host = '0.0.0.0'
port = 5000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections
TIMEOUT_DURATION = 1.0
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)
#
##############

# http://stackoverflow.com/questions/17386487/python-detect-when-a-socket-disconnects-for-any-reason
# http://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python


def ultrasonic_range_measure(GPIO_trigger,GPIO_echo):
    #print('ultrasonic_range_measure...')
    GPIO.output(GPIO_trigger, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_trigger, False)
    start = time.time()
    while GPIO.input(GPIO_echo)==0:
      start = time.time()
    while GPIO.input(GPIO_echo)==1:
        stop = time.time()
        if time.time()-start > 0.1:
            break
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2.0
    return int(distance)




def cleanup_and_exit():
    GPIO.cleanup()
    serversocket.close()
    print(os.path.basename(sys.argv[0])+' : cleaned up.')
    time.sleep(1)
    sys.exit()

last_saccade = time.time()

speed = 0
cruise_control = False
cruise_control_on_t = 0
cruise_speed = 0
cruise_rps = 0

rand_control = False
rand_control_on_t = time.time()
rand_steer = 0

left_range = 0
right_range = 0
rps = 0
steer = 0
speed = 0


def update_driving(buf):
    global last_saccade
    global speed
    global steer
    global cruise_control
    global cruise_control_on_t
    global cruise_speed
    global cruise_rps
    global random_turn_time
    global rand_control
    global rand_control_on_t
    global rand_steer
    global left_range
    global right_range
    global rps
    b = buf.split(' ')
    print b
    if b[3] === 'okay':
        steer = int(b[0])/100.0
        speed = int(b[1])/100.0
        cruise = int(b[2])
    else:
        print(d2s('ERROR, buf =',buf)
        return
    if cruise:
        print "cruise on!!!!"
        cruise_control = True
        cruise_control_on_t = time.time()
        cruise_rps = 3.5#rps
        cruise_speed = speed
    if cruise_control == 1:
        if time.time() - cruise_control_on_t > 1:
#       #     if np.abs(speed) > 0.5:
            if speed < -0.5:
                cruise_control = False
                cruise_control_on_t = 0
                print "CRUISE OFF!!!!!!!"
    if cruise_control:
        #cruise_speed += 0.01*(rps-cruise_rps)
        if rps > 1.1 * cruise_rps:
            cruise_speed -= 0.003
        elif rps < 0.9 * cruise_rps:
            cruise_speed += 0.003
        else:
            pass
        speed = cruise_speed
    if time.time() - rand_control_on_t > 2 and cruise_control:
        print "rand_control!!!!"
        rand_control = True
        rand_control_on_t = time.time()
        rand_steer = (0.5 - 1.0 * np.random.random(1))[0]
    if rand_control:
        if time.time() - rand_control_on_t > 0.75:
            if np.abs(steer) > 0.333:
                rand_control = False
                rand_control_on_t = time.time()
                print "rand_control OFF!!!!!!!"
            else:
                pass#rand_steer = 0.0
    if rand_control:
        steer = rand_steer
    #print drive_data
    print(steer,speed,rps,rand_control,cruise_control)
    servo_ds = 9.43 + 2.0*steer
    motor_ds = 7.0 + 0.75*speed
    pwm_steer.ChangeDutyCycle(servo_ds)
    pwm_motor.ChangeDutyCycle(motor_ds)




reed_close_lst = []
start_t = time.time()
try:
    while True:
        try:
            buf = connection.recv(64)
        except:
            cleanup_and_exit()
        if len(buf) != "":
            if time.time() - start_t >= 1.0:
                d_time = time.time() - start_t
                start_t = time.time()
                rps = reed_close / d_time # / 2.0
                reed_close = 0
            update_driving(buf)
            #left_range = ultrasonic_range_measure(GPIO_TRIGGER_LEFT,GPIO_ECHO_LEFT)
            #right_range = ultrasonic_range_measure(GPIO_TRIGGER_RIGHT,GPIO_ECHO_RIGHT)
            print(d2s('range,rps =',(left_range,right_range,rps)))
        else:
            print("*** No Data received from socket ***")
            cleanup_and_exit()
            break
except KeyboardInterrupt:
    cleanup_and_exit()
