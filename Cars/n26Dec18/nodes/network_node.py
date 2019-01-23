#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import torch
import cv2
import kzpy3.Menu_app.menu2 as menu2
import network_utils.init
import network_utils.menu_and_net
import network_utils.run
import network_utils.camera
if '__file__' not in locals() or __file__ == 'INTERPRETER':
    import kzpy3.Cars.n26Dec18.nodes.Activity_Module as Activity_Module
    import kzpy3.Cars.n26Dec18.nodes.default_values as default_values
    import kzpy3.Cars.n26Dec18.nodes.network_utils.net_utils
    Arguments['desktop_mode']=True
else:
    import network_utils.Activity_Module
    import default_values
exec(identify_file_str)
N = default_values.P
N['desktop_mode'] = False
try:
    if Arguments['desktop_mode']:
        N['desktop_mode'] = True
except:
    Arguments = {}
raw_enter(d2s("N['desktop_mode'] ==",N['desktop_mode'],"\t"))


###################################################################
#
rospy.init_node('network_node',anonymous=True,disable_signals=True)
#
###################################################################



network_utils.init.ros_init(N)

N['behavioral_metadatas'] = network_utils.init.metadata_init()

cm(100)

if __name__ == '__main__':

    N['ABORT'] = False
    cm(101)
    while not rospy.is_shutdown() and N['ABORT'] == False:
        cm(102)
        network_utils.menu_and_net.read_menu_and_load_network(N)

        if network_utils.run.ready(N):

            #camera_data = 

            #metadata = 

            #network_utils.run.step(camera_data,metadata,N)
            print 'run net'
            time.sleep(1)
        else:
            time.sleep(2)

cm(103)
#EOF

    