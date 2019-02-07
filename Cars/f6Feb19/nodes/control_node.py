#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import default_values
import std_msgs.msg
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)

P = default_values.P

###################################################################
#
rospy.init_node('control_node',anonymous=True,disable_signals=True)
#
###################################################################

C = {}

C['net/steer'],C['net/motor'],C['flex/steer'],C['flex/motor'] = 49.,49.,49.,49.
C['ready'] = False

def net_steer_callback(msg):
    C['net/steer'] = msg.data

def net_motor_callback(msg):
    C['net/motor'] = msg.data
    C['ready'] = True

def flex_steer_callback(msg):
    C['flex/steer'] = msg.data

def flex_motor_callback(msg):
    C['flex/motor'] = msg.data


rospy.Subscriber('net/steer', std_msgs.msg.Float32, callback=net_steer_callback)
rospy.Subscriber('net/motor', std_msgs.msg.Float32, callback=net_motor_callback)
rospy.Subscriber('flex/steer', std_msgs.msg.Float32, callback=flex_steer_callback)
rospy.Subscriber('flex/motor', std_msgs.msg.Float32, callback=flex_motor_callback)

C['cmd/steer/pub'] = rospy.Publisher('cmd/steer',std_msgs.msg.Int32,queue_size=5)
C['cmd/motor/pub'] = rospy.Publisher('cmd/motor',std_msgs.msg.Int32,queue_size=5)


print_timer = Timer(0.2)
parameter_file_load_timer = Timer(2)

ctr = 0

if __name__ == '__main__':

    hz = Timer(10)

    while not rospy.is_shutdown() and P['ABORT'] == False:

        if print_timer.check():
            print_timer.reset()
            ctr += 1
            cc = cg
            if C['net/motor'] < 47 and C['flex/motor'] < 47:
                cc = cm
            elif C['net/motor'] < 47:
                cc = cb
            elif C['flex/motor'] < 47:
                cc = cr
            cc(int(C['net/steer']),int(C['net/motor']),int(C['flex/steer']),int(C['flex/motor']))

        if parameter_file_load_timer.check():

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

            parameter_file_load_timer.reset()

def get_adjusted_commands(torch_camera,torch_steer,torch_motor,N):

    if N['use flex'] and N['flex_motor'] < 47:
        #cm(0)
        torch_steer = N['flex_steer'] # consider sum
        torch_motor = N['flex_motor']
        sm = N['flex_motor_smoothing_parameter']
        ss = N['flex_servo_smoothing_parameter']
        gm = N['flex_motor_gain']
        gs = N['flex_steer_gain']
        sc = N['network_camera_smoothing_parameter_direct']
        gc = N['network_camera_gain_direct']
    else:
        sm = N['network_motor_smoothing_parameter']

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

    #print(format_row([('s',adjusted_steer),('c',adjusted_camera),('m',adjusted_motor)]))
    """
    if print_timer.check():
        cg('c:',adjusted_camera,
        '\ts:',adjusted_steer,
        N['mode']['behavioral_mode'],'\tm:',
        adjusted_motor,"\t",file)
        print_timer.reset()
    """
    return adjusted_camera,adjusted_steer,adjusted_motor
#EOF

    