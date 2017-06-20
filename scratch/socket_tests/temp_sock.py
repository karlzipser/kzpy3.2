# from drive_server_RPi.py

from kzpy3.utils import *
print os.path.basename(sys.argv[0])


##############
#
import socket
#import select
host = '0.0.0.0'
port = 5000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections
TIMEOUT_DURATION = 0.333
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)
#
##############

# http://stackoverflow.com/questions/17386487/python-detect-when-a-socket-disconnects-for-any-reason
# http://stackoverflow.com/questions/667640/how-to-tell-if-a-connection-is-dead-in-python


def ultrasonic_range_measure(GPIO_trigger,GPIO_echo):
    #print('ultrasonic_range_measure...')
    enter_time = time.time()
    timeout = 0.1
    GPIO.output(GPIO_trigger, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_trigger, False)
    start = time.time()
    while GPIO.input(GPIO_echo)==0:
      start = time.time()
      if time.time() - enter_time > timeout:
        raise ValueError(d2s('range measure timeout 1'))
    while GPIO.input(GPIO_echo)==1:
        stop = time.time()
        if time.time() - enter_time > timeout:
            raise ValueError(d2s('range measure timeout 1'))
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

begin_time = time.time()

def update_driving(buf):
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
    #print buf
    if b[3] != 'okay':
        sleep_time = 2
        pwm_motor.ChangeDutyCycle(0)
        pwm_steer.ChangeDutyCycle(9)
        time.sleep(0.1)
        pwm_steer.ChangeDutyCycle(10)
        time.sleep(0.1)
        pwm_steer.ChangeDutyCycle(0)
        print(d2s('\a',bcolors.FAIL,'update_driving PROBLEM (buf=[',buf,']. Stopping motor for',sleep_time,'s, . . .',bcolors.ENDC))
        time.sleep(sleep_time)

    steer = int(b[0])/100.0
    speed = int(b[1])/100.0
    cruise = int(b[2])
    if (np.abs(steer) > 1.0) or (np.abs(speed) > 1.0) or cruise > 1:
        raise ValueError(d2s('Bad value from buf:',buf))

    if time.time() - begin_time < 0.5: # there is some problem with the initial cruise being high
        steer = 0
        speed = 0
        cruise = 0

    """
    if left_range < 30:# or right_range < 50:
        if speed > 0:
            steer = 0
            speed = 0
            cruise = 0
            rand_control = False
            print(d2s('Proximity warning, auto stopping!!!!!!!, range =',(left_range,right_range)))
    """
    if cruise:
        print bcolors.WARNING+"cruise on!!!!"+ bcolors.ENDC
        cruise_control = True
        cruise_control_on_t = time.time()
        cruise_rps = rps # 3.5 up to 2/13/16
        cruise_speed = speed
    if cruise_control:
        if time.time() - cruise_control_on_t > 1:
            if np.abs(speed) > 0.5:
                cruise_control = False
                cruise_control_on_t = 0
                print "CRUISE OFF!!!!!!!"
    if cruise_control:
        #cruise_speed += 0.01*(rps-cruise_rps)
        
        if rps > 0:
            cruise_speed += 0.003 * (cruise_rps - rps)/rps
        else:
            cruise_speed += 0.003
        if cruise_speed > 1.0:
            cruise_speed = 1.0
        if cruise_speed < -1.0:
            cruise_speed = -1.0 
        """
        if rps > 1.1 * cruise_rps:
            cruise_speed -= 0.003
        elif rps < 0.9 * cruise_rps:
            cruise_speed += 0.003
        else:
            pass
        """
        
        speed = cruise_speed

    if False:  # rand_control
        if time.time() - rand_control_on_t > 2 and cruise_control and not rand_control: # was 2 before 2/13/16
            print "rand_control!!!!"
            rand_control = True
            rand_control_on_t = time.time()
            #rand_steer = (0.5 - 1.0 * np.random.random(1))[0] #before 13Feb2016
            rand_steer = (0.25 - 0.5 * np.random.random(1))[0]
            GPIO.output(GPIO_LED1, True)
        if rand_control:
            if time.time() - rand_control_on_t > 0.75:
                if np.abs(steer) > 0.2:#333:
                    rand_control = False
                    rand_control_on_t = time.time()
                    print "rand_control OFF!!!!!!!"
                    GPIO.output(GPIO_LED1, False)
                else:
                    pass#rand_steer = 0.0
        if rand_control:
            steer = rand_steer
    

    drive_data = d2n('Begin _str=',int(steer*100),'_spd=',int(speed*100),
        '_rps=',int(rps*10),'_lrn=',int(left_range),'_rrn=',int(right_range),
        '_rnd=',int(rand_control),'_ End')

    drive_success = False
    fail_ctr = 0
    fail_t = time.time()
    while drive_success == False:
        try:
            list_of_strings_to_txt_file("/home/pi/drive_data.txt",[drive_data,'okay'])
            drive_success = True
        except Exception, e:
            fail_ctr += 1
            print(d2s('fail time =',time.time()-fail_t,'fail ctr =',fail_ctr,drive_data_strs,os.path.basename(sys.argv[0]),':',e))

    #print drive_data

    print(steer,dec2(speed),dec2(rps),dec2(cruise_rps),rand_control,cruise_control)
    servo_ds = 9.43 + 2.0*steer
    motor_ds = 7.0 + 0.75*speed
    assert(motor_ds) <= 7.0+0.75
    assert(motor_ds) >= 7.0-0.75
    pwm_steer.ChangeDutyCycle(servo_ds)
    pwm_motor.ChangeDutyCycle(motor_ds)
    """
    GPIO.output(GPIO_LED1, False)
    GPIO.output(GPIO_LED2, False)
    if steer > 0.50:
        GPIO.output(GPIO_LED1, True)
    elif steer < -0.50:
        GPIO.output(GPIO_LED2, True)
    """



reed_close_lst = []
start_t = time.time()
try:
    while True:
        okay = False
        try:
            buf = ''
            t0 = time.time()
            while len(buf) < 64:
                buf += connection.recv(64)
                if time.time()-t0 > 0.5:
                    print("""\a stuck in 'while len(buf) < 64' """)
                    raise Exception(d2s("""stuck in 'while len(buf) < 64' """,buf))
                    t0 = time.time()
            assert len(buf) == 64
            buf = buf.strip('?')
            okay = True
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e,' \a ######### pwm_motor.ChangeDutyCycle(0)'))
            #buf = '0 0 0 PROBLEM'
            #print(d2s(bcolors.FAIL,'############################# Setting buf to',buf,bcolors.ENDC))
            pwm_motor.ChangeDutyCycle(0)
            #cleanup_and_exit()
        if okay:
            if len(buf) != "":
                if time.time() - start_t >= 1.0:
                    d_time = time.time() - start_t
                    start_t = time.time()
                    rps = reed_close / d_time  / 2.0 # two magnets
                    reed_close = 0
                #print((reed_close_times,2.0*(reed_close_times[1]-reed_close_times[0])))
                rps = 1.0/(2.0*(reed_close_times[1]-reed_close_times[0]))
                if time.time() - reed_close_times[1] > 1:
                    rps = 0

                update_driving(buf)
                """
                try:
                    left_range = ultrasonic_range_measure(GPIO_TRIGGER_LEFT,GPIO_ECHO_LEFT)
                except Exception, e:
                    print e
                """
                #right_range = ultrasonic_range_measure(GPIO_TRIGGER_RIGHT,GPIO_ECHO_RIGHT)
                #print(d2s('range =',(dec2(left_range))))#,right_range,rps)))
            else:
                print("\a *** No Data received from socket ***")
                cleanup_and_exit()
                break
except KeyboardInterrupt:
    print(d2s(os.path.basename(sys.argv[0]),':','KeyboardInterrupt \a'))
    cleanup_and_exit()

"""
        reed_close = 0
        start_t = time.time()

        time.sleep(1)

        d_time = time.time() - start_t
        if len(reed_close_lst) < 2:
            reed_close_lst.append((reed_close,d_time))
        else:
            advance(reed_close_lst,(reed_close,d_time))
        cnt = 0
        dt = 0
        for r in reed_close_lst:
            cnt += r[0]
            dt += r[1]
        print cnt / dt
"""


