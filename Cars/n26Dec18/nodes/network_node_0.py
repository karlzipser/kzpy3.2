from kzpy3.vis3 import *
import rospy
rospy.init_node('network_node',anonymous=True,disable_signals=True)
import network_node_1
import network_node_1b
import network_node_1c

threading.Thread(target=network_node_1.fun,args=[]).start()
threading.Thread(target=network_node_1b.fun,args=[]).start()
threading.Thread(target=network_node_1c.fun,args=[]).start()
