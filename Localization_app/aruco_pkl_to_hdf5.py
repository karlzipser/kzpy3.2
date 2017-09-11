


def load_Aruco_Steering_Trajectories():
	print("Loading Aruco_Steering_Trajectories . . .")
	paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
	Aruco_Steering_Trajectories = {}
	ctr = 0
	for p in paths:
		o = lo(p)
		run_name = fname(p).replace('.pkl','')
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		Aruco_Steering_Trajectories[run_name] = {}
		for mode in ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']:
			Aruco_Steering_Trajectories[run_name][mode] = {}
			for direction in [0,1]:
				Aruco_Steering_Trajectories[run_name][mode][direction] = {}
				for t in o[mode][direction]:
					for l in o[mode][direction][t]:
						if l in ['steer','motor']:
							Aruco_Steering_Trajectories[run_name][mode][direction][t] = {}
							Aruco_Steering_Trajectories[run_name][mode][direction][t][l] = o[mode][direction][t][l]
		ctr += 1
		#if ctr > 5:
		#	break
	return Aruco_Steering_Trajectories



if True:
	Aruco_Steering_Trajectories = load_Aruco_Steering_Trajectories()
	so(Aruco_Steering_Trajectories,opjD('Aruco_Steering_Trajectories.pkl'))



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
			#steer_list = []
			for t in time_stamps:
				#	steer_list.append(Aruco_Steering_Trajectories[r][m][d][t]['steer'])
				G = F.create_group(opj(r,m,str(d),t))
				steer = Aruco_Steering_Trajectories[r][m][d][t]['steer']
				print steer
				G.create_dataset('steer',data=na(steer))
				print G
				#F[opj(r,m,str(d))].create_dataset('ts',data=na(time_stamps))
				#F[opj(r,m,str(d))].create_dataset('steer',data=na(steer_list))
				#clf();plot(time_stamps,steer_list);plt.title(r);spause();
F.close()
print timer.time()



#############################


timer = Timer(0)
runs = sorted(Aruco_Steering_Trajectories.keys())
modes = ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']
directions = [0,1]
del_list = []
for r in runs:
	for m in modes:
		for d in directions:
			time_stamps = sorted(Aruco_Steering_Trajectories[r][m][d].keys())
			for t in time_stamps:
				for k in Aruco_Steering_Trajectories[r][m][d][t]:
					if k not in ['steer','motor']:
						del_list.append([r,m,d,t,k])
so(Aruco_Steering_Trajectories,opjD('Aruco_Steering_Trajectories_concise'))
print timer.time()
