from kzpy3.vis3 import *

import kzpy3.Data_app.lidar.python_pointclouds6i as ppc

for a in Arguments:
    ppc.A[a] = Arguments[a]

ppc.rospy.init_node('receive_pointclouds')
ppc.rospy.Subscriber('/os1_node/points', ppc.PointCloud2, ppc.points__callback)

threading.Thread(target=ppc.pointcloud_thread,args=[]).start()

while ppc.A['ABORT'] == False:
	if 'e'  in ppc.Output:
	    mci(
	        (z2o(ppc.Output['e'].transpose(1,0))*255).astype(np.uint8),
	        scale=1.0,
	        color_mode=cv2.COLOR_GRAY2BGR,
	    )
	    mi(ppc.Output['e'].transpose(1,0));spause()
	    cr(shape(ppc.Output['e']))
cg("pc_main.py")