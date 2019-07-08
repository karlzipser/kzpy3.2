#!/usr/bin/env python

"""
http://wiki.ros.org/rosbag/Commandline
rosbag info
rosbag play -r 2
# -s SEC, --start=SEC
# -u SEC, --duration=SEC
# --skip-empty=SEC
# -l, --loop

rosbag play -s 5 recorded1.bag
"""

from kzpy3.utils3 import *
assert HAVE_ROS
try:
	bagpath = Arguments['path']
except:
	from kzpy3.scripts.__local__.bagpath_local import bagpath
	
cg("\nStarting roscore...\n")
os.system("roscore &")
time.sleep(3)
cg("\nShort wait before starting bag loop\n")
time.sleep(3)

timer = Timer(hour)

while not timer.check():
	sys_str = "rosbag play "+bagpath+"/*.bag"
	cg(sys_str)
	os.system(sys_str)

cg("\nbagloop complete.\n")

#EOF
