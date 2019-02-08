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

C = {}

for src in ['net','flex']:
    for typ in ['steer','motor']:
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
C['heading'] = 0.
C['reference_heading'] = 0.
C['distance'] = 0.
C['reference_distance'] = 0.
C['human_agent'] = 1
C['drive_mode'] = 0
C['behavioral_mode'] = 'ghost'
C['human_agent/prev'] = 1
C['drive_mode/prev'] = 0
C['button_number/prev'] = 2
C['behavioral_mode/prev'] = 'ghost'
C['behavioral_mode/timer'] = Timer()
C['drive_mode/timer'] = Timer()
C['human_agent/timer'] = Timer()
C['button_number/timer'] = Timer()

C['ready'] = False
C['encoder_time'] = 0.0
C['encoder_time_prev'] = 0.0

bcs = '/bair_car'

def net_steer_callback(msg):
    C['net/steer'] = msg.data

def net_motor_callback(msg):
    C['net/motor'] = msg.data
    C['ready'] = True

def flex_steer_callback(msg):
    C['flex/steer'] = msg.data

def flex_motor_callback(msg):
    C['flex/motor'] = msg.data

s = 0.9
def encoder_callback(msg):
    C['encoder'] = msg.data
    C['encoder_time'] = time.time()
    C['distance'] += C['encoder'] * (C['encoder_time']-C['encoder_time_prev'])
    C['encoder_time_prev'] = C['encoder_time']
    C['encoder/smooth'] = (1.0-s)*C['encoder'] + s*C['encoder/smooth']

def gyro_heading_callback(msg):
    C['heading'] = msg.x

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
    C['button_number/prev'] = C['button_number']

"""
def behavioral_mode_callback(msg):
    C['behavioral_mode'] = msg.data
    if C['behavioral_mode'] != C['behavioral_mode/prev']:
        C['behavioral_mode/timer'].reset()
        C['reference_heading'] = C['heading']
        C['reference_distance'] = C['distance']
    C['behavioral_mode/prev'] = C['behavioral_mode']
"""



rospy.Subscriber('net/steer', std_msgs.msg.Float32, callback=net_steer_callback)
rospy.Subscriber('net/motor', std_msgs.msg.Float32, callback=net_motor_callback)
rospy.Subscriber('flex/steer', std_msgs.msg.Float32, callback=flex_steer_callback)
rospy.Subscriber('flex/motor', std_msgs.msg.Float32, callback=flex_motor_callback)
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder_callback)
rospy.Subscriber(bcs+'/human_agent',std_msgs.msg.Int32,callback=human_agent_callback)
rospy.Subscriber(bcs+'/button_number',std_msgs.msg.Int32,callback=button_number_callback)
#rospy.Subscriber(bcs+'/behavioral_mode',std_msgs.msg.String,callback=behavioral_mode_callback)
rospy.Subscriber(bcs+'/drive_mode',std_msgs.msg.Int32,callback=drive_mode_callback)
rospy.Subscriber(bcs+'/gyro_heading',geometry_msgs.msg.Vector3,callback=gyro_heading_callback)
C['cmd/steer/pub'] = rospy.Publisher('cmd/steer',std_msgs.msg.Int32,queue_size=5)
C['cmd/motor/pub'] = rospy.Publisher('cmd/motor',std_msgs.msg.Int32,queue_size=5)
C['behavioral_mode_pub'] = rospy.Publisher(bcs+'behavioral_mode', std_msgs.msg.String, queue_size=5)

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
        raw_enter()
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
        sp = ' '
        if C['net/motor'] < 47:
            nm = rd
        if C['flex/motor'] < 47:
            fm = rd
        if C['encoder'] < 0.01:
            en = rd
        if error > 0:
            er = rd
        pd2n(
            er,error,sp,
            #ns,int(C['net/steer']),sp,
            nm,int(C['net/motor']),sp,
            #fs,int(C['flex/steer']),sp,
            fm,int(C['flex/motor']),sp,
            en,dp(C['encoder']),sp,
            bl,C['error_count'],sp,
            gr,dp(C['encoder/smooth']),sp,
            lb,dp(C['heading']-C['reference_heading']),sp,
            gr,C['button_number'],sp,
            gr,dp(C['distance']-C['reference_distance']),sp,
        )


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







if __name__ == '__main__':

    while not rospy.is_shutdown() and P['ABORT'] == False:

        if C['ready']:

            C['ready'] = False

            for src in ['net','flex']:
                for typ in ['steer','motor']:
                    val,error = check_value(C[opj(src,typ)],0,99,-20,119,49.)
                    C[opj(src,typ,'check')] = val
                    C[opj(src,typ,'error')] = error

            print_topics()

            check_menu()




#EOF

    