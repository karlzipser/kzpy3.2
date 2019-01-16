from kzpy3.vis3 import *
import rospy
rospy.init_node('network_node',anonymous=True,disable_signals=True)
import network_node__
import network_node_ldr__

while True:
    network_node__.step()
    #network_node_ldr__.step()


