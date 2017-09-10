F = h5w(opjD('Aruco_Steering_Trajectories.hdf5'))
from kzpy3.vis2 import *
runs = sorted(Aruco_Steering_Trajectories.keys())
modes = ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']
directions = [0,1]

timer = Timer(0)
for r in runs:
	for m in modes:
		for d in directions:
			time_stamps = sorted(Aruco_Steering_Trajectories[r][m][d].keys())
			steer_list = []
			for t in time_stamps:
				steer_list.append(Aruco_Steering_Trajectories[r][m][d][t]['steer'])
			F[opj(r,m,str(d))].create_dataset('ts',data=na(time_stamps))
			F[opj(r,m,str(d))].create_dataset('steer',data=na(steer_list))
			clf();plot(time_stamps,steer_list);plt.title(r);spause();
F.close()
print timer.time()
