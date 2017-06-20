from kzpy3.utils import *
from kzpy3.teg1.camera import *
import serial

if '/Users/' in home_path:
    ser = serial.Serial('/dev/tty.usbmodem1461',9600) #115200)
else:
    ser = serial.Serial('/dev/ttyACM0',9600)

STATE_LOCK = 2
STATE_LOCK_CALIBRATE = 4
STATE_HUMAN_FULL_CONTROL = 1
STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR = 3
STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR = 5

caffe_int = -30000
camera_off_flag = True
caffe_mode = 1 # no function for now



def encode_int_signal(caffe_mode,caffe_steer,caffe_motor):
    assert(caffe_mode >= -3 and caffe_mode <= 3 )
    assert(caffe_steer >=0 and caffe_steer < 100)
    assert(caffe_motor >=0 and caffe_motor < 100)
    return 10000*caffe_mode + 100*caffe_steer + caffe_motor

unix('mkdir -p ' + opjD('teg_data'))

subprocess.Popen(['python',opjh('kzpy3/teg1/sensor_worker.py')])

f = open(opjD('teg_data','_'+time_str()+'.motor_servo.txt'), 'w')

while True:
    try:
        ser.write(d2s('(',caffe_int,')'))
        s = ser.readline()
        exec('t = ' + s)
        assert(type(t) == tuple)
        t = list(t)
        t.append(time.time())
        f.write(d2s(t,'\n'))
        #print t
        in_state = t[0]
        in_steer = t[1]
        in_motor = t[2]

        scale_factor = 1.0
        if in_state == STATE_HUMAN_FULL_CONTROL:
            if camera_off_flag:
                camera_on(opjh('Desktop/teg_data',time_str()))
                camera_off_flag = False
                np.save(opjh('Desktop/caffe_quit_command.npy'),1)
        elif in_state == STATE_LOCK or in_state == STATE_LOCK_CALIBRATE:
            if camera_off_flag == False:
                camera_off()
                camera_off_flag = True
                np.save(opjh('Desktop/caffe_quit_command.npy'),1)
        elif in_state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR or in_state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR:
            if camera_off_flag:
                camera_on(opjh('Desktop/teg_data',time_str()))
                camera_off_flag = False
                np.save(opjh('Desktop/caffe_quit_command.npy'),0)
                subprocess.Popen(['python',opjh('kzpy3/teg1/caffe_worker.py')])

        caffe_steer = int(np.load(opjh('Desktop/caffe_command.npy')))
        #print caffe_steer
        out_steer = 49+caffe_steer
        out_motor = in_motor
        caffe_int = encode_int_signal(caffe_mode,out_steer,out_motor)
    except Exception,e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))

