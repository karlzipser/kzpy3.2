from kzpy3.utils import *
from kzpy3.teg1.camera import *
import serial

"""
This hub program on host computer commuicates with Arduino running motor_servo_2.cpp.
It turns on and off the Caffe process and other sensor process.

Communication between this control program and Caffe is done via text files:

    ~/Desktop/caffe_quit_command.npy (command to Caffe to issue quit command)
    ~/Desktop/caffe_command.npy (Caffe's commands to be sent to the car via Arduino)

This is for simplicity. In the future, a more mature mutli-process or threading
approach would be appropriate.
"""

"""
Two kinds of complications with serial communication with multple Arduinos.
OsX and ubuntu have different ways of 
specifying serial port. And, on ubuntu, the ACM# depends on both
the order of the USBs in the ports and the order in which they
are plugged in (if plugged in after booting.) 
Thus, it would be good to have some error checking to insure the correct
device is connected to the correct host program. If not, the wrong Arduino will provide
serial input to a given host program.
"""
BAUD = 115200
TIMEOUT = 0.25
if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1461',BAUD,timeout=TIMEOUT)
else:
    ser = serial.Serial('/dev/ttyACM0',BAUD,timeout=TIMEOUT)

# These state codes must match those in the motor_servo Arduino code.
"""
#define STATE_HUMAN_FULL_CONTROL            1
#define STATE_LOCK                          2
#define STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR 3
#define STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR 5
#define STATE_LOCK_CALIBRATE                4
#define STATE_ERROR                         -1
"""
STATE_HUMAN_FULL_CONTROL     =       1
STATE_LOCK                   =      2
STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR = 3
STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR = 5
STATE_LOCK_CALIBRATE              =  4
STATE_ERROR                       =  -1

# Some intial variable values
caffe_int = -30000 # i.e., mode = -3, steer = 0, motor = 0
camera_off_flag = True
quit_caffe = 1
caffe_mode = 1 # no function for now

# Put three numbers into an int to send to Arduino
def encode_int_signal(caffe_mode,caffe_steer,caffe_motor):
    assert(caffe_mode >= -3 and caffe_mode <= 3 )
    assert(caffe_steer >=0 and caffe_steer < 100)
    assert(caffe_motor >=0 and caffe_motor < 100)
    return 10000*caffe_mode + 100*caffe_steer + caffe_motor

# Ensure data director exists
unix('mkdir -p ' + opjD('teg_data'))

# The GPS+ Arduino host program is set running here.
subprocess.Popen(['python',opjh('kzpy3/teg1/sensor_worker.py')])

# Data file for motor/servo data
f = open(opjD('teg_data','_'+time_str()+'.motor_servo.txt'), 'w')

ctr = 0
while True:
    try:
        ser.write(d2s('(',caffe_int,')'))
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        t = list(t)
        t.append(time.time())
        
        ctr += 1
        in_state = t[0]
        in_steer = t[1]
        in_motor = t[2]
        in_state_change_time = t[3]
        assert( in_state >= -1 and in_state < 100)
        assert( in_steer >= 0 and in_steer < 100)
        assert( in_motor >= 0 and in_motor < 100)
        assert( in_state_change_time >= 0 )
        if in_state == STATE_HUMAN_FULL_CONTROL:
            # Wait before turning on camera.
            if camera_off_flag and in_state_change_time >= 1:
                camera_on(opjh('Desktop/teg_data',time_str()))
                print 'camera on'
                camera_off_flag = False
                quit_caffe = 1
                np.save(opjh('Desktop/caffe_quit_command.npy'),quit_caffe)
        elif in_state == STATE_LOCK or in_state == STATE_LOCK_CALIBRATE:
            if camera_off_flag == False:
                camera_off()
                print 'camera off'
                camera_off_flag = True
                quit_caffe = 1
                np.save(opjh('Desktop/caffe_quit_command.npy'),quit_caffe)
        elif in_state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR or in_state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR:
            # Wait before turning on camera and Caffe.
            if camera_off_flag and in_state_change_time >= 1:
                camera_on(opjh('Desktop/teg_data',time_str()))
                print 'camera on'
                camera_off_flag = False
                quit_caffe = 0
                np.save(opjh('Desktop/caffe_quit_command.npy'),quit_caffe)
                subprocess.Popen(['python',opjh('kzpy3/teg1/caffe_worker.py')])
        if camera_off_flag == False and quit_caffe == 0:
            caffe_steer = int(np.load(opjh('Desktop/caffe_command.npy')))
        else:
            caffe_steer = 0
        #out_steer = 49 + caffe_steer # Note, polarity can flip depending on RC transmitter settings!
        out_steer = 49 - caffe_steer # Note, polarity can flip depending on RC transmitter settings!
        out_motor = in_motor
        # Note, error checking on these control values occurs in encode_int_signal.
        caffe_int = encode_int_signal(caffe_mode,out_steer,out_motor)
        t.append(caffe_mode)
        t.append(out_steer)
        t.append(out_motor)
        f.write(d2s(t,'\n'))
        if np.mod(ctr,100) == 0: # Print output, but not too much of it.
            print t
    except Exception,e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))

