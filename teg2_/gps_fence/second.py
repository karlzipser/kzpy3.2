# export ROS_MASTER_URI=http://192.168.43.113:11311

from kzpy3.teg2.global_run_params import *
from kzpy3.teg2.gps_fence.geometry import *
from kzpy3.vis import *
from kzpy3.teg2.global_run_params import *
import roslib
import std_msgs.msg
import rospy
"""
GPS2_lat = -999.9
GPS2_long = 0
GPS2_speed = 0
GPS2_angle = 0

def GPS2_lat_callback(msg):
	global GPS2_lat
	GPS2_lat = msg.data


rospy.init_node('listener',anonymous=True)

rospy.Subscriber('GPS2_lat', std_msgs.msg.Float32, callback=GPS2_lat_callback)


while not rospy.is_shutdown():
	try:
		print GPS2_lat
		time.sleep(0.5)
	except Exception as e:
		print e.message, e.args
"""
#os.environ["ROS_MASTER_URI"] = "http://192.168.43.113:11311"

GPS2_lat = -999.99
GPS2_long = -999.99
GPS2_speed = -999.99
GPS2_angle = -999.99

def GPS2_lat_callback(msg):
	global GPS2_lat
	GPS2_lat = msg.data
	
def GPS2_long_callback(msg):
	global GPS2_long
	GPS2_long = msg.data
	
def GPS2_speed_callback(msg):
	global GPS2_speed
	GPS2_speed = msg.data
	
def GPS2_angle_callback(msg):
	global GPS2_angle
	GPS2_angle = msg.data

steer_list = []
#Msg = None
def steer_callback(msg):
	global steer_list
	#global Msg
	steer_list.append(msg.data)
	if len(steer_list) > 100:
		steer_list = steer_list[-100:]
	#Msg = msg

#rospy.init_node('listener',anonymous=True)



#rospy.Subscriber('/bair_car/steer', std_msgs.msg.Int32, callback=steer_callback)

rospy.Subscriber('/bair_car/GPS2_lat', std_msgs.msg.Float32, callback=GPS2_lat_callback)
rospy.Subscriber('/bair_car/GPS2_long', std_msgs.msg.Float32, callback=GPS2_long_callback)
rospy.Subscriber('/bair_car/GPS2_speed', std_msgs.msg.Float32, callback=GPS2_speed_callback)
rospy.Subscriber('/bair_car/GPS2_angle', std_msgs.msg.Float32, callback=GPS2_angle_callback)
plt.ion()

#from kzpy3.teg2.rospy_metacode import *
#exec ros_str

miles_per_deg_lat = 68.94
miles_per_deg_lon_at_37p88 = 54.41
meters_per_mile = 1609.34

GPS2_lat_orig,GPS2_long_orig = 37.8814506531,-122.27844238
GPS2_lat_orig,GPS2_long_orig = 37.9166107178,-122.334060669
GPS2_lat_orig,GPS2_long_orig = 37.8831100464, -122.273178101
rng = 300
xorg = 0
yorg = 0
dx = 0
dy = 0
plt.figure(1)

#plt.xlim(GPS2_long_orig-rng,GPS2_long_orig+rng)
#plt.ylim(GPS2_lat_orig-rng,GPS2_lat_orig+rng)
plt.xlim(-rng+xorg,rng+xorg)
plt.ylim(-rng+yorg,rng+yorg)
plt_square()
ctr = 0

time_step_step = 0.4
t0 = time.time()
time_step =  False
while not rospy.is_shutdown():
	if time.time() - time_step > time_step_step:
		time_step = True
		t0 = time.time()
	if time_step:
		txt = txt_file_to_list_of_strings(opj('kzpy3/teg2/gps_fence/second_params.py'))
		str = ''
		for t in txt:
			str += t + '\n'
		exec(str)

	
	
	plt.subplot(1,2,2)
	plt.cla()
	
	#plt.xlim(0,99)
	plt.ylim(0,99)

	try:
		time_points = np.arange(0,len(steer_list)*0.015,0.015)
		time_points -= time_points[-1]
		plot([time_points[0],time_points[-1]],[49,49],'r')
		plot(time_points,steer_list,'b')
	except:
		print (len(time_points),len(steer_list))

	plt.pause(0.01)
	if time_step:
		#print gyro_msg['y']
		try:
			print GPS2_lat,GPS2_long,GPS2_speed,GPS2_angle
			if GPS2_lat > -999:
				dx = (GPS2_lat-GPS2_lat_orig)*miles_per_deg_lat*meters_per_mile
				dy = (GPS2_long-GPS2_long_orig)*miles_per_deg_lon_at_37p88*meters_per_mile
				rp = rotatePoint([dx,dy],[dx+1,dy],GPS2_angle)
				if np.mod(ctr,2) == 0:
					clr = 'r'
				else:
					clr = 'k'
				#plt.plot(dy,dx,clr+'o')
				plt.subplot(1,2,1)
				plt_square()
				plt.plot([dy,rp[1]],[dx,rp[0]],clr)
			#plt.pause(0.5);#time.sleep(0.5)
		except Exception as e:
			print e.message, e.args
	ctr += 1
	if time_step:
		xorg = dx
		yorg = dy
		plt.ylim(-rng+xorg,rng+xorg)
		plt.xlim(-rng+yorg,rng+yorg)



raw_input()


gps_data = ['lat','long','speed','angle']

for g in gps_data:
	print "GPS2_"+g+" = -999.99"

for g in gps_data:
	print """def GPS2_"""+g+"""_callback(msg):
	global GPS2_"""+g+"""
	GPS2_"""+g+""" = msg.data
	"""

for g in gps_data:
	print """rospy.Subscriber('/bair_car/GPS2_"""+g+"""', std_msgs.msg.Float32, callback=GPS2_"""+g+"""_callback)"""

