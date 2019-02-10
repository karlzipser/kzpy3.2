from kzpy3.utils3 import *

from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge,CvBridgeError



Pub = {}
for side in ['left','right']:
    Pub[side] = rospy.Publisher("/bair_car/zed/"+side+"/image_rect_color",Image,queue_size=1)
def Mock_ZEDpublish(P,index):
    for side in ['left','right']:
        if P['desktop version/artifical mode']:
            img = np.random.randn(94,168,3)
        else:
            img = P['desktop version/O'][side+'_image']['vals'][P['desktop version/index']]
        img = z2_255(img)
        Pub[side].publish(CvBridge().cv2_to_imgmsg(img,'rgb8'))


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
    bpwm = 870
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



Timers = {'MSE':Timer(1/30.),'IMU':Timer(1/30./3.),'FLEX':Timer(1/30./12.)}







class Mock_Arduino:

    def __init__(self,P,atype):
        self.P = P
        self.atype = atype
        self.servo_pers = []
        self.motor_pers = []
    def write(self,write_str):
        if self.P['desktop version/pwm to screen']:
            if self.atype == 'MSE':
                #print write_str
                w2 = write_str.replace(')','')
                w2 = w2.replace('(','')
                l = w2.split(',')
                servo_pwm = int(l[0])
                camera_pwm = int(l[1])-5000
                motor_pwm = int(l[2])-10000

                servo_per = 100-servo_pwm/2000.*100
                camera_per = 100-camera_pwm/2000.*100
                motor_per = motor_pwm/2000.*100
                
                if False:
                    self.servo_pers.append(servo_per)
                    self.motor_pers.append(motor_per)

                    servo_median,motor_median = 0,0
                    if len(self.servo_pers) > 100:
                        servo_median = np.median(self.servo_pers)
                    if len(self.servo_pers) > 6000:
                        self.servo_pers = self.servo_pers[-5000:]
                    if len(self.motor_pers) > 100:
                        motor_median = np.median(self.motor_pers)
                    if len(self.motor_pers) > 5000:
                        self.motor_pers = self.motor_pers[-5000:]
                    
                    lst = [
                        (str(self.P['button_number']),0),
                        ('S',servo_per),
                        ('C',camera_per),
                        ('M',motor_per),
                        ('.',servo_median),
                        ('.',motor_median),
                    ]
                    np.random.shuffle(lst)
                    row_str = format_row(lst)
                    if self.P['agent_is_human']:
                        cprint(row_str,'red')
                    else:
                        cprint(row_str,'green')
                
                    
    def readline(self):
        _ = self.P
        if self.P['desktop version/artifical mode']:
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
            Mock_ZEDpublish(_,0)
            time.sleep(1/30.)
            return rstr
        else:
            while _['ABORT'] == False:
                L = _['desktop version/L']
                index = _['desktop version/index']
                if self.atype == 'MSE' and Timers['MSE'].check():
                    Timers['MSE'].reset()
                    _['desktop version/index'] += 1
                    if _['desktop version/index'] >= len(L['steer']):
                        _['desktop version/index'] = _['desktop version/start index']#+1
                    index = _['desktop version/index']
                    servo_pwm = servo_percent_to_pwm(L['steer'][index],_)
                    motor_pwm = motor_percent_to_pwm(L['motor'][index],_)
                    encoder = L['encoder'][index]
                    button_pwm = button_number_to_pwm(L['button_number'][index])
                    rstr = d2c("('mse'",button_pwm,servo_pwm,motor_pwm,encoder)+")"
                    Mock_ZEDpublish(_,index)
                    break
                elif self.atype == 'FLEX' and Timers['FLEX'].check():
                    Timers['FLEX'].reset()
                    n = np.random.choice(flex_names)
                    if n in L:
                        rstr = "('"+d2c(n+"'",L[n][index])+')'
                    else:
                        rstr = ""
                    break
                elif self.atype == 'IMU' and Timers['IMU'].check():
                    Timers['IMU'].reset()
                    n = np.random.choice(imu_names)
                    rstr = "('"+d2c(n+"'",L[n+'_x'][index],L[n+'_y'][index],L[n+'_z'][index])+')'
                    break
                else:
                    time.sleep(1/30./30.)
            return rstr


    def flushInput(self):
        pass

    def flushOutput(self):
        pass


def put_mock_Arduinos_into_P(P):
    P['Arduinos'] = {}
    for a in ['MSE','FLEX','IMU','LIGHTS']:
        P['Arduinos'][a] = Mock_Arduino(P,a)



#EOF


