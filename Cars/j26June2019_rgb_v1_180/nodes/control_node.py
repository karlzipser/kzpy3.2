#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import default_values
import std_msgs.msg
import geometry_msgs.msg
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)

P = default_values.P

###################################################################
#
rospy.init_node('control_node',anonymous=True,disable_signals=True)
#
###################################################################
green_for_from_still_motor_offset = False
purple_for_gyro_heading_callback = False
green_for_forward = True
purple_for_reverse = True
green_and_purple_for_still = True

vel_encoding_coeficient = 1.0/2.3

DIRECT = 2
LEFT = 1
RIGHT = 3
GHOST = 4
UNKNOWN = 5
BLUE = 100
WHITE = 101
GREEN = 102
PURPLE = 103
BLUE_OFF = 104
WHITE_OFF = 105
GREEN_OFF = 106
PURPLE_OFF = 107

C = {}

for src in ['net','flex']:
    for typ in ['steer','motor','camera','steer/smooth','motor/smooth','camera/smooth']:
        C[opj(src,typ)] = 49.
for src in ['net','flex']:
    for typ in ['steer','motor','camera']:
        C[opj(src,typ,'error')] = 0
for src in ['net','flex']:
    for typ in ['steer','motor','camera']:
        C[opj(src,typ,'check')] = 49.

C['from still motor offset'] = 0.
C['from still motor offset timer'] = Timer(1)
C['error_count'] = 0
C['encoder'] = 0.
C['encoder/error'] = 0
C['encoder/smooth'] = 0.
C['velocity'] = 0.
C['heading'] = 0.
C['reference_heading'] = 0.
C['distance'] = 0.
C['reference_distance'] = 0.
C['human_agent'] = 1
C['drive_mode'] = 0
C['behavioral_mode'] = GHOST
C['human/steer'] = 49
C['drive_direction'] = 0
C['behavior_names'] = {
    LEFT:'left',
    RIGHT:'right',
    DIRECT:'direct',
    GHOST:'ghost',
    UNKNOWN:'unknown',
}

C['lights'] = {
    DIRECT: 'left right red',
    LEFT:   'left right red, left blink yellow',
    RIGHT:  'left right red, right blink yellow',
    GHOST:  'left right blink yellow',
    BLUE:   'blue',
    WHITE:  'white',
    GREEN:  'green',
    PURPLE: 'purple',
    BLUE_OFF:   'blue off',
    WHITE_OFF:  'white off',
    GREEN_OFF:  'green off',
    PURPLE_OFF: 'purple off',
}

for c in ['blue','white','purple','green']:
    C[c+' is on'] = False
    C[c+' timer'] = Timer(0.5)
C['human_agent/prev'] = 1
C['drive_mode/prev'] = 0
C['button_number'] = 4
C['button_number/prev'] = 4
C['behavioral_mode/prev'] = GHOST
C['behavioral_mode/timer'] = Timer()
C['behavioral_mode_pub_timer'] = Timer(2/30.)
C['lights_pub_ready'] = False
C['drive_mode/timer'] = Timer()
C['human_agent/timer'] = Timer()
C['button_number/timer'] = Timer()
C['still_timer'] = Timer()
C['collision_timer'] = Timer()
C['new_motor'] = 49
C['new_steer'] = 49
C['new_camera'] = 49
C['pre saccade camera prev'] = 49
C['pre saccade camera'] = 49
C['ready'] = False
C['encoder_time'] = time.time()
C['encoder_time_prev'] = time.time() - 1/30.

bcs = '/bair_car'

C['cmd/steer/pub'] = rospy.Publisher('cmd/steer',std_msgs.msg.Int32,queue_size=5)
C['cmd/motor/pub'] = rospy.Publisher('cmd/motor',std_msgs.msg.Int32,queue_size=5)
C['cmd/camera/pub'] = rospy.Publisher('cmd/camera',std_msgs.msg.Int32,queue_size=5)
C['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
C['lights_pub'] = rospy.Publisher('lights', std_msgs.msg.String, queue_size=5)








def net_steer_callback(msg):
    C['net/steer'] = msg.data
    C['net/camera'] = C['net/steer']

def net_motor_callback(msg):
    C['net/motor'] = msg.data
    if C['net/motor'] < 49:
        if C['blue is on'] == False:
            C['lights_pub'].publish(C['lights'][BLUE])
            C['blue is on'] = True
            C['blue timer'].reset()
    elif C['blue is on'] == True and C['blue timer'].check():
        C['lights_pub'].publish(C['lights'][BLUE_OFF])
        C['blue is on'] = False
    

def flex_steer_callback(msg):
    C['flex/steer'] = msg.data


C['white timer'] = Timer(0.25)
def flex_motor_callback(msg):
    C['flex/motor'] = msg.data
    
    if C['flex/motor'] < P['flex/motor collision threshold']:
        C['collision_timer'].reset()
    if C['flex/motor'] < P['flex/motor white light threshold']:
        if C['white is on'] == False:
            C['white timer'].reset()
            C['lights_pub'].publish(C['lights'][WHITE])
            C['white is on'] = True
    if C['white is on'] == True and C['white timer'].check():
        C['lights_pub'].publish(C['lights'][WHITE_OFF])
        C['white is on'] = False
    


s = 0.9
def encoder_callback(msg):

    C['encoder'] = msg.data

    C['encoder_time'] = time.time()

    C['encoder/smooth'] = (1.0-s)*C['encoder'] + s*C['encoder/smooth']
    C['velocity'] = vel_encoding_coeficient * C['encoder/smooth']
    if C['new_motor'] < 49:
        C['velocity'] *= -1.
    if np.abs(C['velocity']) > 0.1:
        C['still_timer'].reset()

    C['distance'] += C['velocity'] * (C['encoder_time']-C['encoder_time_prev'])
    C['encoder_time_prev'] = C['encoder_time']


C['turned'] = False
C['purple on'] = False

def gyro_heading_callback(msg):
    C['heading'] = msg.x

    C['behavioral_mode/prev'] = C['behavioral_mode']

    if C['button_number'] == 1:
        if C['heading']-C['reference_heading'] > P['d_heading_for_end_turning'] or C['turned']:
            C['behavioral_mode'] = DIRECT
            C['turned'] = True
            # Light gets turned off in Arduino so need to keep turning it on.
            if purple_for_gyro_heading_callback:
                C['lights_pub'].publish(C['lights'][PURPLE])
            C['purple on'] = True
        else:
            C['behavioral_mode'] = LEFT
            if C['purple on']:
                if purple_for_gyro_heading_callback:
                    C['lights_pub'].publish(C['lights'][PURPLE_OFF])
                C['purple on'] = False

    elif C['button_number'] == 3:
        if C['heading']-C['reference_heading'] < -P['d_heading_for_end_turning'] or C['turned']:
            C['behavioral_mode'] = DIRECT
            C['turned'] = True
            # Light gets turned off in Arduino so need to keep turning it on.
            if True:#not C['purple on']: 
                C['lights_pub'].publish(C['lights'][PURPLE])
                #print 'purple'
                C['purple on'] = True
        else:
            C['behavioral_mode'] = RIGHT
            if C['purple on']:
                C['lights_pub'].publish(C['lights'][PURPLE_OFF])
                C['purple on'] = False

    elif C['button_number'] == 2:
        C['behavioral_mode'] = DIRECT
        C['turned'] = False
        if C['purple on']:
            C['lights_pub'].publish(C['lights'][PURPLE_OFF])
            C['purple on'] = False
                
    elif C['button_number'] == 4:
        C['behavioral_mode'] = GHOST
        C['turned'] = False
        if C['purple on']:
            C['lights_pub'].publish(C['lights'][PURPLE_OFF])
            C['purple on'] = False
    else:
        C['behavioral_mode'] = UNKNOWN
        C['turned'] = False

    if C['behavioral_mode/prev'] != C['behavioral_mode']:
        C['lights_pub_ready'] = True


def human_agent_callback(msg):
    C['human_agent'] = msg.data
    if C['human_agent'] != C['human_agent/prev']:
        C['human_agent/timer'].reset()
    C['human_agent/prev'] = C['human_agent']


def drive_mode_callback(msg):
    C['drive_mode'] = msg.data
    if C['drive_mode'] != C['drive_mode/prev']:
        C['drive_mode/timer'].reset()
    C['drive_mode/prev'] = C['drive_mode']


def button_number_callback(msg):
    C['button_number'] = msg.data
    if C['button_number'] != C['button_number/prev']:
        C['button_number/timer'].reset()
        C['reference_heading'] = C['heading']
        C['reference_distance'] = C['distance']
    C['button_number/prev'] = C['button_number']


def human_steer_callback(msg):
    C['human/steer'] = msg.data

def drive_direction_callback(msg):
    C['drive_direction'] = msg.data



rospy.Subscriber('/net/steer', std_msgs.msg.Float32, callback=net_steer_callback)
rospy.Subscriber('/net/motor', std_msgs.msg.Float32, callback=net_motor_callback)
rospy.Subscriber('/flex/steer', std_msgs.msg.Float32, callback=flex_steer_callback)
rospy.Subscriber('/flex/motor', std_msgs.msg.Float32, callback=flex_motor_callback)
rospy.Subscriber(bcs+'/encoder', std_msgs.msg.Float32, callback=encoder_callback)
rospy.Subscriber(bcs+'/human_agent',std_msgs.msg.Int32,callback=human_agent_callback)
rospy.Subscriber(bcs+'/button_number',std_msgs.msg.Int32,callback=button_number_callback)
rospy.Subscriber(bcs+'/drive_mode',std_msgs.msg.Int32,callback=drive_mode_callback)
rospy.Subscriber(bcs+'/gyro_heading',geometry_msgs.msg.Vector3,callback=gyro_heading_callback)
rospy.Subscriber(bcs+'/steer', std_msgs.msg.Int32, callback=human_steer_callback)
rospy.Subscriber('/drive_direction',std_msgs.msg.Int32,callback=drive_direction_callback)

print_timer = Timer(0.2)
parameter_file_load_timer = Timer(2)



def check_menu():
    if parameter_file_load_timer.check():
        parameter_file_load_timer.reset()
        Topics = menu2.load_Topics(
            P['project_path'],
            first_load=False,
            customer='Control')
        if type(Topics) == dict:
            for t in Topics['To Expose']['Network']+\
                     Topics['To Expose']['Weights']+\
                     Topics['To Expose']['Flex']+\
                     Topics['To Expose']['Control']+\
                     Topics['To Expose']['Arduino']:
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
            vrb = True
            if not P['control print']:
                vrb = False
            for c in ['yellow','green','blue','magenta','cyan','white','Grey']:
                CVerbose[c] = vrb


def check_value(val,mn,mx,mn_err,mx_err,default):
    error = 0
    if int(val) > mx_err or int(val) < mn_err:
        error = 1
        val = default
    else:
        val = bound_value(val,mn,mx)
    return val,error



def print_topics():
    if not P['control print']:
        return
    if print_timer.check():
        print_timer.reset()
        error = 0
        for src in ['net','flex']:
            for typ in ['steer','motor','camera']:
                error += C[opj(src,typ,'error')]
        C['error_count'] += error
        er = bl
        nm = gr
        ns = gr
        fm = lb
        fs = lb
        en = yl
        nmo = gr
        sp = ' '
        if C['net/motor'] < 47:
            nm = rd
        if C['flex/motor'] < 47:
            fm = rd
        if C['encoder'] < 0.01:
            en = rd
        if error > 0:
            er = rd
        if C['new_motor'] < 49:
            nmo = rd
        pd2n(
            nm,'net/mo ',int(C['net/motor']),sp,
            fm,'flex/mo ',int(C['flex/motor']),sp,
            nmo,'new_mo ',int(C['new_motor']),sp,
            nmo,'new_cam ',int(C['new_camera']),sp,
            rd,'still ',dp(C['from still motor offset']),sp,
            yl,'vel ',dp(C['velocity'],1),sp,
            #mg,dp(C['still_timer'].time(),1),sp,
            #gr,dp(C['collision_timer'].time(),1),sp,
            #lb,'ref hd ',int(C['heading']-C['reference_heading']),sp,
            #rd,C['button_number'],sp,
            rd,C['behavior_names'][C['behavioral_mode']],sp,
            #gr,'dist ',dp(C['distance']-C['reference_distance'],1),sp,
            #rd,C['error_count'],sp,
            #yl,C['from still motor offset'],sp,
        )



def from_still_motor_offset():
    """
    If the car is not moving, some random action may get it back on
    course. This is expressed as C['from still motor offset'] which
    will be added to the motor command.
    """
    if C['still_timer'].time() > 1.0:
        if C['from still motor offset'] < 0.1:
            C['from still motor offset timer'].reset()
            C['from still motor offset'] = np.random.choice([10.,-10.])
            if green_for_from_still_motor_offset:
                C['lights_pub'].publish(C['lights'][GREEN])
            #cy('GREEN')
    elif not C['from still motor offset timer'].check():
        C['from still motor offset'] *= 0.99 # note depends on run speed
    else:
        if np.abs(C['from still motor offset']) > 0:
            if green_for_from_still_motor_offset:
                C['lights_pub'].publish(C['lights'][GREEN_OFF])
                #cy('GREEN OFF')
        C['from still motor offset'] = 0.   





def adjusted_motor():
    
    from_still_motor_offset()
    still_motor_offset = P['still_motor_offset_gain'] * C['from still motor offset']
    
    flex = C['flex/motor']
    flex = min(49,flex)
    flex = P['flex_motor_gain']*(flex-49) + 49
    s = P['flex_motor_smoothing_parameter']
    C['flex/motor/smooth'] = (1.0-s)*flex + s*C['flex/motor/smooth']
    C['flex/motor/smooth'] = bound_value(C['flex/motor/smooth'],0,49)

    motor = C['net/motor']
    s = P['network_motor_smoothing_parameter']
    if motor > 49:
        if C['behavioral_mode'] == DIRECT:
            gain = P['network_motor_gain_direct']
        else:
            gain = P['network_motor_gain']
    else:
        gain = P['network_reverse_motor_gain']

    motor = gain*(motor-49) + 49
    C['net/motor/smooth'] = (1.0-s)*motor + s*C['net/motor/smooth']
    C['net/motor/smooth'] = bound_value(C['net/motor/smooth'],0,99)

    new_motor = C['net/motor/smooth'] + C['flex/motor/smooth']-49 + still_motor_offset
    if new_motor > 50:
        new_motor += P['network_motor_offset']
    elif new_motor < 47:
        new_motor += P['network_reverse_motor_offset']

    if P['max motor'] < 49:
        P['max motor'] = 49
        cr("*** Error, P['max motor'] < 49")
    if P['min motor'] > 49:
        P['min motor'] = 49
        cr("*** Error, P['min motor'] > 49")
    new_motor = bound_value(intr(new_motor),P['min motor'],P['max motor'])
    C['new_motor'] = new_motor






def adjusted_steer():

    steer = C['net/steer']

    if C['behavioral_mode'] == DIRECT:
        gain = P['network_steer_gain_direct']
        if C['velocity'] > 1.1:
            gain *= 1.0
        elif C['velocity'] < 0.33:
            gain *= 4.0
        elif C['velocity'] < 0.66:
            gain *= 2.0
        # also, slow down when turning to damp ossilations
        s = P['network_servo_smoothing_parameter_direct']
    else:
        gain = P['network_steer_gain']
        s = P['network_servo_smoothing_parameter']

    steer = gain*(steer-49) + 49

    C['net/steer/smooth'] = (1.0-s)*steer + s*C['net/steer/smooth']

    if C['flex/motor/smooth'] < P['flex/motor collision threshold']:
        new_steer = bound_value(intr(C['flex/steer']),0,99)
    else:
        new_steer = bound_value(intr(C['net/steer/smooth']),0,99)
        if C['new_motor'] < 49:
            new_steer = 99-new_steer            

    C['new_steer'] = new_steer
    
    ###################
    # TEMP
    if True:
        C['new_steer'] = bound_value(intr(C['net/steer/smooth']),0,99)
    #
    ###################
    





C['saccade timer'] = Timer(1)

def adjusted_camera():

    camera = C['net/camera']

    if C['behavioral_mode'] == DIRECT:
        gain = P['network_camera_gain_direct']
        if C['velocity'] < 0.33:
            gain = P['low velocity direct steer gain']
        s = P['network_camera_smoothing_parameter']
    else:
        gain = P['network_camera_gain']
        s = P['network_camera_smoothing_parameter']

    camera = gain*(camera-49) + 49

    C['net/camera/smooth'] = (1.0-s)*camera + s*C['net/camera/smooth']


    C['pre saccade camera prev'] = C['pre saccade camera']


    if C['button_number'] != 4:
        new_camera = bound_value(intr(C['net/camera/smooth']),0,99)
     # 27April2019
    else:
        new_camera = C['human/steer']

    C['pre saccade camera'] = new_camera

    camera_delta = C['pre saccade camera'] - C['pre saccade camera prev']

    if False:
        if np.abs(C['new_camera']-new_camera) > 30:
            if np.abs(C['new_camera']-49) > np.abs(new_camera-49):
                new_camera = 49
                C['saccade timer'].trigger()

    if C['saccade timer'].check():
        C['saccade timer'].time_s = min(0.8,P['saccade timer parameter']*(np.abs(camera_delta)/49.*1000. + 200)/1000.)
        C['saccade timer'].reset()
        #cy("C['saccade timer'].reset()")
        C['new_camera'] = new_camera
    else:
        pass
        #cg("not C['saccade timer'].check()",int(1000*C['saccade timer'].time_s),camera_delta)

    ###################
    # TEMP
    if False:
        C['new_camera'] = bound_value(intr(C['net/camera/smooth']),0,99)
    #
    ###################






if __name__ == '__main__':
    ready = Timer(1/30.)
    while not rospy.is_shutdown() and P['ABORT'] == False:
        try:
            if ready.check():
                ready.reset()
                #print C['drive_direction']
                if C['drive_direction'] < 0:
                    C['lights_pub'].publish(C['lights'][PURPLE])
                    C['lights_pub'].publish(C['lights'][GREEN_OFF])
                elif C['drive_direction'] > 0:
                    C['lights_pub'].publish(C['lights'][PURPLE_OFF])
                    C['lights_pub'].publish(C['lights'][GREEN])
                else:
                    C['lights_pub'].publish(C['lights'][PURPLE])
                    C['lights_pub'].publish(C['lights'][GREEN])

                if C['behavioral_mode_pub_timer'].check():
                    C['behavioral_mode_pub_timer'].reset()
                    C['behavioral_mode_pub'].publish(C['behavior_names'][C['behavioral_mode']])

                if C['lights_pub_ready'] == True:
                    C['lights_pub'].publish(C['lights'][C['behavioral_mode']])
                    C['lights_pub_ready'] = False

                for src in ['net','flex']:
                    for typ in ['camera','steer','motor']:
                        val,error = check_value(C[opj(src,typ)],0,99,-20,119,49.)
                        C[opj(src,typ,'check')] = val
                        C[opj(src,typ,'error')] = error

                adjusted_motor()
                adjusted_steer()
                adjusted_camera()

                C['cmd/motor/pub'].publish(C['new_motor'])
                C['cmd/steer/pub'].publish(C['new_steer'])
                C['cmd/camera/pub'].publish(C['new_camera'])

                print_topics()

                check_menu()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno,int(time.time())),emphasis=False)    
            time.sleep(1)

raw_enter('control_node done.')
#EOF

    