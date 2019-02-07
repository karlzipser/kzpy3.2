#!/usr/bin/env python

from kzpy3.utils3 import *
import default_values
_ = default_values.P
import std_msgs.msg
import geometry_msgs.msg
import rospy
import sensor_msgs.msg
exec(identify_file_str)

###########################################################################################
#
wait = Timer(10)
def setup():
    ccm('setting up')
    _['data_saving'] = 0
    _['data_saving_prev'] = 0
    _['data_saving changed up'] = False
    _['ready'] = False
    def cmd_steer_callback(msg):
        _['cmd/steer'] = msg.data
    def cmd_camera_callback(msg):
        _['cmd/camera'] = msg.data
    def cmd_motor_callback(msg):
        _['cmd/motor'] = msg.data
        _['ready'] = True
    def data_saving_callback(msg):
        _['data_saving_prev'] = _['data_saving']
        _['data_saving'] = msg.data
        if _['data_saving'] == 1 and _['data_saving_prev'] == 0:
            _['data_saving changed up'] = True

    rospy.init_node('format',anonymous=True,disable_signals=True)
    rospy.Subscriber('/cmd/steer', std_msgs.msg.Int32, callback=cmd_steer_callback)
    rospy.Subscriber('/cmd/camera', std_msgs.msg.Int32, callback=cmd_camera_callback)
    rospy.Subscriber('/cmd/motor', std_msgs.msg.Int32, callback=cmd_motor_callback)
    rospy.Subscriber('/bair_car/data_saving', std_msgs.msg.Int32, callback=data_saving_callback)
    time.sleep(1)
    wait.reset()

setup()

wait = Timer(10)

while True:
    if _['ready']:
        _['ready'] = False
        print(format_row([
            ('s',100-_['cmd/steer']),
            ('c',100-_['cmd/camera']),
            ('m',_['cmd/motor'])]))
        wait.reset()
    else:
        time.sleep(0.0001)
        if wait.check():
            rospy.signal_shutdown('wait')
            setup()


#EOF
