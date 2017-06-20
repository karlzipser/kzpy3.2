#!/usr/bin/env python
import roslib; roslib.load_manifest('bair_car')
import rospy

from bair_car.arduino import Arduino

if __name__ == '__main__':
    rospy.init_node('run_arduino', anonymous=True)
    ard = Arduino()
    rospy.spin()
    
