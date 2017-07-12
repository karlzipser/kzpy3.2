from kzpy3.utils2 import *

"""
for n in [0,1,2,3,4,5,6,7,8,9]:#[0,1,2,3,4]:
	os.system(d2s("xterm -hold -e python",opjh('kzpy3/teg9/arena/planner/top_controller.py'),n,'&'))
	pause(2)
"""

for n in [0,1,2,3,4,5,6,7]:
	os.system(d2s("xterm -hold -e python",opjh('kzpy3/teg9/train_with_hdf5_and_aruco_trajectories__collect_data.py'),'-p',n,'&'))
	pause(2)