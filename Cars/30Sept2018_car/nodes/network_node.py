#!/usr/bin/env python
from kzpy3.utils3 import *

import rospy

rospy.init_node('network_node',anonymous=True,disable_signals=True)


while not rospy.is_shutdown():
    time.sleep(5)
