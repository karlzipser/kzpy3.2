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
    for typ in ['steer','motor','steer/smooth','motor/smooth']:
        C[opj(src,typ)] = 49.
for src in ['net','flex']:
    for typ in ['steer','motor']:
        C[opj(src,typ,'error')] = 0
for src in ['net','flex']:
    for typ in ['steer','motor']:
        C[opj(src,typ,'check')] = 49.
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

C['ready'] = False
C['encoder_time'] = time.time()
C['encoder_time_prev'] = time.time() - 1/30.

bcs = '/bair_car'

def net_steer_callback(msg):
    C['net/steer'] = msg.data

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
    C['ready'] = True

def flex_steer_callback(msg):
    C['flex/steer'] = msg.data

def flex_motor_callback(msg):
    C['flex/motor'] = msg.data
    if C['flex/motor'] < 40:
        C['collision_timer'].reset()
        if C['white is on'] == False:
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
    if C['velocity'] > 0.1:
        C['still_timer'].reset()
    C['distance'] += C['velocity'] * (C['encoder_time']-C['encoder_time_prev'])
    C['encoder_time_prev'] = C['encoder_time']




def gyro_heading_callback(msg):
    C['heading'] = msg.x

    C['behavioral_mode/prev'] = C['behavioral_mode']

    if C['button_number'] == 1 or C['button_number'] == 3:

        if np.abs(C['heading']-C['reference_heading']) > P['d_heading_for_end_turning']:
            C['behavioral_mode'] = DIRECT
        elif C['button_number'] == 1:
            C['behavioral_mode'] = LEFT
        elif C['button_number'] == 3:
            C['behavioral_mode'] = RIGHT
    elif C['button_number'] == 2:
        C['behavioral_mode'] = DIRECT
    elif C['button_number'] == 4:
        C['behavioral_mode'] = GHOST
    else:
        C['behavioral_mode'] = UNKNOWN
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




rospy.Subscriber('/bair_car/net/steer', std_msgs.msg.Float32, callback=net_steer_callback)
rospy.Subscriber('/bair_car/net/motor', std_msgs.msg.Float32, callback=net_motor_callback)
rospy.Subscriber('/bair_car/flex/steer', std_msgs.msg.Float32, callback=flex_steer_callback)
rospy.Subscriber('/bair_car/flex/motor', std_msgs.msg.Float32, callback=flex_motor_callback)
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder_callback)
rospy.Subscriber(bcs+'/human_agent',std_msgs.msg.Int32,callback=human_agent_callback)
rospy.Subscriber(bcs+'/button_number',std_msgs.msg.Int32,callback=button_number_callback)
rospy.Subscriber(bcs+'/drive_mode',std_msgs.msg.Int32,callback=drive_mode_callback)
rospy.Subscriber(bcs+'/gyro_heading',geometry_msgs.msg.Vector3,callback=gyro_heading_callback)

C['cmd/steer/pub'] = rospy.Publisher('cmd/steer',std_msgs.msg.Int32,queue_size=5)
C['cmd/motor/pub'] = rospy.Publisher('cmd/motor',std_msgs.msg.Int32,queue_size=5)
C['behavioral_mode_pub'] = rospy.Publisher('behavioral_mode', std_msgs.msg.String, queue_size=5)
C['lights_pub'] = rospy.Publisher('lights', std_msgs.msg.String, queue_size=5)

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
        

def check_value(val,mn,mx,mn_err,mx_err,default):
    error = 0
    if int(val) > mx_err or int(val) < mn_err:
        error = 1
        val = default
    else:
        val = bound_value(val,mn,mx)
    return val,error


def print_topics():
    if print_timer.check():
        print_timer.reset()
        error = 0
        for src in ['net','flex']:
            for typ in ['steer','motor']:
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
            #er,error,sp,
            #ns,int(C['net/steer']),sp,
            nm,int(C['net/motor']),sp,
            #fs,int(C['flex/steer']),sp,
            fm,int(C['flex/motor']),sp,
            nmo,C['new_motor'],sp,
            yl,dp(C['velocity'],1),sp,
            mg,dp(C['still_timer'].time(),1),sp,
            gr,dp(C['collision_timer'].time(),1),sp,
            lb,int(C['heading']-C['reference_heading']),sp,
            rd,C['button_number'],sp,
            rd,C['behavior_names'][C['behavioral_mode']],sp,
            gr,dp(C['distance']-C['reference_distance'],1),sp,
            rd,C['error_count'],sp,
        )


def adjusted_motor():

    flex = C['flex/motor']
    flex = min(49,flex)
    flex = P['flex_motor_gain']*(flex-49) + 49
    s = P['flex_motor_smoothing_parameter']
    C['flex/motor/smooth'] = (1.0-s)*flex + s*C['flex/motor/smooth']

    motor = C['net/motor']
    motor = P['network_motor_gain']*(motor-49) + 49
    s = P['network_motor_smoothing_parameter']
    C['net/motor/smooth'] = (1.0-s)*motor + s*C['net/motor/smooth']

    new_motor = C['net/motor/smooth'] + C['flex/motor/smooth']-49

    new_motor = bound_value(intr(new_motor),P['min motor'],P['max motor'])

    return new_motor



if __name__ == '__main__':

    while not rospy.is_shutdown() and P['ABORT'] == False:

        if C['ready']:

            if C['behavioral_mode_pub_timer'].check():
                C['behavioral_mode_pub_timer'].reset()
                C['behavioral_mode_pub'].publish(C['behavior_names'][C['behavioral_mode']])
            
            if C['lights_pub_ready'] == True:
                C['lights_pub'].publish(C['lights'][C['behavioral_mode']])
                C['lights_pub_ready'] = False

            C['ready'] = False

            for src in ['net','flex']:
                for typ in ['steer','motor']:
                    val,error = check_value(C[opj(src,typ)],0,99,-20,119,49.)
                    C[opj(src,typ,'check')] = val
                    C[opj(src,typ,'error')] = error

            C['new_motor'] = adjusted_motor()

            print_topics()

            check_menu()


"""
collisions

def Driving(C):
    D = {}
    return D

def Not_Moving_Motor_Off(C):
    D = {}
    return D

def Not_Moving_Motor_On(C):
    D = {}
    return D

def Repeated_Collisions(C):
    D = {}

def Driving_Backwards(C):
    D = {}
"""




"""
def get_adjusted_commands(torch_camera,torch_steer,torch_motor,N):


        N['flex_motor_smoothing_parameter']
        N['flex_servo_smoothing_parameter']
        N['flex_motor_gain']
        N['flex_steer_gain']
        N['network_camera_smoothing_parameter_direct']
        N['network_camera_gain_direct']
        N['network_motor_smoothing_parameter']

        if torch_motor >= 49:
            if N['mode']['behavioral_mode'] == 'direct':
                gm = N['network_motor_gain_direct']
            else:
                gm = N['network_motor_gain']
        else:
            gm = N['network_reverse_motor_gain']

        if N['mode']['behavioral_mode'] == 'direct':
            ss = N['network_servo_smoothing_parameter_direct']
            gs = N['network_steer_gain_direct']
            gc = N['network_camera_gain_direct']          
            sc = N['network_camera_smoothing_parameter_direct']
        else:
            ss = N['network_servo_smoothing_parameter']
            gs = N['network_steer_gain']
            gc = N['network_camera_gain']          
            sc = N['network_camera_smoothing_parameter']


    N['current']['camera'] = (1.0-sc)*torch_camera + sc*N['current']['camera']
    N['current']['steer'] = (1.0-ss)*torch_steer + ss*N['current']['steer']
    N['current']['motor'] = (1.0-sm)*torch_motor + sm*N['current']['motor']

    adjusted_motor = int(gm*(N['current']['motor']-49) + N['network_motor_offset'] + 49)
    adjusted_steer = int(gs*(N['current']['steer']-49) + 49)
    adjusted_camera = int(gc*(N['current']['camera']-49) + 49)

    adjusted_motor = bound_value(adjusted_motor,0,99)
    adjusted_steer = bound_value(adjusted_steer,0,99)
    adjusted_camera = bound_value(adjusted_camera,0,99)

    adjusted_motor = min(adjusted_motor,N['max motor'])
    adjusted_motor = max(adjusted_motor,N['min motor'])
"""
    #print(format_row([('s',adjusted_steer),('c',adjusted_camera),('m',adjusted_motor)]))
"""
    if print_timer.check():
        cg('c:',adjusted_camera,
        '\ts:',adjusted_steer,
        N['mode']['behavioral_mode'],'\tm:',
        adjusted_motor,"\t",file)
        print_timer.reset()
    
    return adjusted_camera,adjusted_steer,adjusted_motor
"""










#EOF

    