###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3'])
#
###############################
from kzpy3.vis2 import *
import roslib
import std_msgs.msg
import rospy
from kzpy3.Localization_app.Parameters_Module import *
exec(identify_file_str)
na = np.array
"""
export ROS_MASTER_URI=http://192.168.1.20:11311
make sure master's ip and name (tegra-ubuntu) are in /etc/hosts
on master, export ROS_IP=0.0.0.0 # Listen on any interface
"""
ipaddr_ = "http://192.168.1.20:11311"
print(d2s('Setting ROS_MASTER_URI to',ipaddr_))
os.environ["ROS_MASTER_URI"] = ipaddr_
os.environ["ROS_IP"] = "0.0.0.0"

R = {}
for k_ in [aruco_position_x,aruco_position_y,aruco_heading_x,aruco_heading_y]:
	R[k_] = {ts:[],vals:[]}

def aruco_position_x__callback(msg):
	R[aruco_position_x][ts].append(time.time())
	R[aruco_position_x][vals].append(msg.data)
def aruco_position_y__callback(msg):
	R[aruco_position_y][ts].append(time.time())
	R[aruco_position_y][vals].append(msg.data)
def aruco_heading_x__callback(msg):
	R[aruco_heading_x][ts].append(time.time())
	R[aruco_heading_x][vals].append(msg.data)
def aruco_heading_y__callback(msg):
	R[aruco_heading_y][ts].append(time.time())
	R[aruco_heading_y][vals].append(msg.data)
rospy.init_node('listener',anonymous=True)
rospy.Subscriber('/bair_car/aruco_position_x', std_msgs.msg.Float32, callback=aruco_position_x__callback)
rospy.Subscriber('/bair_car/aruco_position_y', std_msgs.msg.Float32, callback=aruco_position_y__callback)
rospy.Subscriber('/bair_car/aruco_heading_x', std_msgs.msg.Float32, callback=aruco_heading_x__callback)
rospy.Subscriber('/bair_car/aruco_heading_y', std_msgs.msg.Float32, callback=aruco_heading_y__callback)

pts_ = []
for k_ in Marker_xy_dic.keys():
	if not is_number(k_):
		pts_.append(Marker_xy_dic[k_])
pts_ = na(pts_)
pts_plot(pts_,'b')
raw_enter()
ctr_ = 0

while True:
	try:
		x_ = R[aruco_position_x][vals][-1]
		y_ = R[aruco_position_y][vals][-1]
		hx_ = R[aruco_heading_x][vals][-1] + x_
		hy_ = R[aruco_heading_y][vals][-1] + y_
			

		figure(5);clf();plt_square();xysqlim(2*107.0/100.0);
		plot(hx_,hy_,'g.')
		plot(x_,y_,'r.')
		pts_plot(pts_,'b')
		pause(0.0001)
		ctr_ += 1
		if np.mod(ctr_,100) == 0:
			spd2s(ctr_/timer_.time(),'hz')
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)

