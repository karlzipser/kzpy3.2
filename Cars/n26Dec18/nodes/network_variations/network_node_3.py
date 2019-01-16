from kzpy3.vis3 import *
import rospy
rospy.init_node('network_node',anonymous=True,disable_signals=True)
import network_node__
#import network_node_ldr__

while True:
    network_node__.step()
    #network_node_ldr__.step()


if False:
    from kzpy3.vis3 import *
    import rospy
    rospy.init_node('network_node',anonymous=True,disable_signals=True)
    Arguments['desktop_mode']=True
    import kzpy3.Cars.n26Dec18.nodes.network_node__ as network_node__#import network_node_ldr__

    network_node__.step()



