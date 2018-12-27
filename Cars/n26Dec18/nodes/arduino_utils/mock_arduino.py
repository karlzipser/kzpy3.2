from kzpy3.utils3 import *

###################### duplicates ########################
#
flex_names = [
    'FL0',
    'FL1',
    'FL2',
    'FL3',
    'FR0',
    'FR1',
    'FR2',
    'FR3',
    'FC0',
    'FC1',
    'FC2',
    'FC3',
]
def percent_to_pwm(percent,null_pwm,max_pwm,min_pwm):
    if percent >= 49:
        p = (percent-50)/50.0 * (max_pwm-null_pwm) + null_pwm
    else:
        p = (percent-50)/50.0 * (null_pwm-min_pwm) + null_pwm
    return p

def servo_percent_to_pwm(percent,P):
    return percent_to_pwm(percent,P['servo_pwm_null'],P['servo_pwm_max'],P['servo_pwm_min'])

def motor_percent_to_pwm(percent,P):
    return percent_to_pwm(percent,P['motor_pwm_null'],P['motor_pwm_max'],P['motor_pwm_min'])

def button_number_to_pwm(bn):
    if bn == 1:
        bpwm = 1900
    elif bn == 2:
        bpwm = 1700
    elif bn == 3:
        bpwm = 1424
    elif bn == 4:
        bpwm = 870
    return bpwm

#
############################################################

imu_names = ['acc','gyro','head']

artifical_mode = True

Timers = {'MSE':Timer(1/30.),'IMU':Timer(1/30./3.),'FLEX':Timer(1/30./12.)}

class Mock_Arduino:

    def __init__(self,P,atype):
        self.P = P
        self.atype = atype

    def write(self,write_str):
        pass

    def readline(self):
        _ = self.P
        if artifical_mode:
            a = np.sin(time.time()/5.)*400+1200
            b = np.sin(time.time()/15.)*400+1200
            c = np.sin(time.time()/30.)*1.0+3.0
            d = np.sin(time.time()*2)
            if self.atype == 'MSE':
                rstr = d2c("('mse'",1700,a,b,c,")")
            elif self.atype == 'FLEX':
                rstr = "('"+d2c(np.random.choice(flex_names)+"'",b+500)+')'
            elif self.atype == 'IMU':
                rstr = "('"+d2c(np.random.choice(imu_names)+"'",d,d,d)+')'
            #print rstr
            return rstr
        else:
            while _['ABORT'] == False:
                if self.atype == 'MSE' and Timer('MSE').check():
                    Timer('MSE').reset()
                    L = _['desktop version/L']
                    _['desktop version/index prev'] = _['desktop version/index']
                    _['desktop version/index'] += 1
                    if _['desktop version/index'] >= len(L['steer']):
                        _['desktop version/index'] = 1
                        _['desktop version/index prev'] = 0
                    index = _['desktop version/index']
                    index_prev = _['desktop version/index prev']
                    servo_pwm = servo_percent_to_pwm(L['steer'][index],_)
                    motor_pwm = motor_percent_to_pwm(L['motor'][index],_)
                    encoder = L['encoder'][index]
                    button_pwm = button_number_to_pwm(L['button_number'][index])
                    rstr = d2c("('mse'",button_pwm,servo_pwm,motor_pwm,encoder)+")"
                    Mock_ZEDpublish(_,index)

                elif self.atype == 'FLEX' and Timer('FLEX').check():
                    Timer('FLEX').reset()
                    n = np.random.choice(flex_names)
                    rstr = "('"+d2c(n+"'",L[n][index])+')'

                elif self.atype == 'IMU' and Timer('IMU').check():
                    Timer('IMU').reset()
                    n = np.random.choice(imu_names)
                    rstr = "('"+d2c(n+"'",L[n+'_x'][index],L[n+'_y'][index],L[n+'_z'][index])+')'
                else:
                    time.sleep(1/30./30.)
            #print rstr
            return rstr


    def flushInput(self):
        pass

    def flushOutput(self):
        pass


def put_mock_Arduinos_into_P(P):
    P['Arduinos'] = {}
    for a in ['MSE','FLEX','IMU','SOUND']:
        P['Arduinos'][a] = Mock_Arduino(P,a)



from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge,CvBridgeError
Pub = {}
for side in ['left','right']:
    Pub[side] = rospy.Publisher("/zed/"+side+"/image_rect_color",Image,queue_size=1)
def Mock_ZEDpublish(P,index):
    print "mz"
    for side in ['left','right']:
        img = P['desktop version/O'][side+'_image']['vals'][P['desktop version/index']]
        img = z2_255(img)
        Pub['side'].publish(CvBridge().cv2_to_imgmsg(img,'rgb8'))


def Mock_ZED():
    while True:
        print "mz"
        time.sleep(1/30.)
        img = np.random.randn(94,168,3)
        img = z2_255(img)
        pub.publish(CvBridge().cv2_to_imgmsg(img,'rgb8'))

#EOF


