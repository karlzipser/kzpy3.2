from kzpy3.utils2 import *


data_path = Args['PATH']

def load_Aruco_Steering_Trajectories(data_path):
	print("Loading Aruco_Steering_Trajectories . . .")
	paths = sggo(data_path,'Aruco_Steering_Trajectories','*.pkl')
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
	return Aruco_Steering_Trajectories



if True:
	Aruco_Steering_Trajectories = load_Aruco_Steering_Trajectories(data_path)
	so(Aruco_Steering_Trajectories,opj(data_path,'Aruco_Steering_Trajectories.pkl'))

"""
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
"""


#############################

"""
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
"""







##################################################################################
#
for car in ['Mr_Purple','Mr_Black','Mr_Blue','Mr_Lt_Blue','Mr_Orange','Mr_Yellow']:

	all_left_timestamps = []
	folders5 = sggo(data_path,'h5py','*')
	for f in folders5:
		if car in f:
			try:
				F = h5r(opj(f,'left_timestamp_metadata_right_ts.h5py'))
				time_stamps = list(F['ts'][:])
				assert(len(time_stamps)>0)
				all_left_timestamps += time_stamps
				F.close()
			except Exception as e:
				print("********** Exception ***********************")
				print(e.message, e.args)

	all_aruco_left_timestamps = []
	folders = sggo(data_path,'Aruco_Steering_Trajectories','*')
	for f in folders:
		if car in f:
			try:
				o = lo(f)
				for r in o.keys():
					for b in o[r]:
						for t in o[r][b]:
							all_aruco_left_timestamps.append(t)
			except Exception as e:
				print("********** Exception ***********************")
				print(e.message, e.args)



	common_timestamps = sorted(list(set(all_left_timestamps) & set(all_aruco_left_timestamps)))
	valid_timestamps = []
	valid_timestamp_pairs = {}
	for i in range(0,len(common_timestamps)-1):
		if common_timestamps[i+1] - common_timestamps[i] < 1/30.*3.0:
			valid_timestamps.append(common_timestamps[i])
			valid_timestamp_pairs[common_timestamps[i]] = common_timestamps[i+1]
	print len(valid_timestamps)/30./60./60.

	so(opj(data_path,'valid_timestamps.'+car+'.pkl'),valid_timestamps)
	so(opj(data_path,'valid_timestamp_pairs.'+car+'.pkl'),valid_timestamp_pairs)



	valid_timestamps = lo(opj(data_path,'valid_timestamps.'+car+'.pkl'))
	data_moments = []
	folders = sggo(data_path,'Aruco_Steering_Trajectories','*')

	for f in folders:
		print f
		try:
			run_name = fname(f).split('.')[0]
			if car in run_name:
				o = lo(f)
				for r in o.keys():
					for b in o[r]:
						for t in o[r][b]:
							if t in valid_timestamps:
								steer = o[r][b][t]['steer']
								motor = o[r][b][t]['motor']
								data_moments.append((run_name,t,r,b,steer,motor))
							else:
								print t,'invalid'
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)
	so(data_moments,opj(data_path,'data_moments_'+car))
#
##################################################################################






####################left ######################
#
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print f
	left_timestamp_index_dic = {}
	try:
		F = h5r(opj(f,'left_timestamp_metadata_right_ts.h5py'))
		time_stamps = list(F['ts'][:])
		assert(len(time_stamps)>0)
		ctr = 0
		for t in time_stamps:
			left_timestamp_index_dic[t] = ctr
			ctr += 1
			#print ctr
		F.close()
		print (len(left_timestamp_index_dic.values()),max(left_timestamp_index_dic.values()))
		so(left_timestamp_index_dic,opj(f,'left_timestamp_index_dic'))
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
#
##########################################
#################### right ######################
#
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print f
	right_timestamp_index_dic = {}
	try:
		F = h5r(opj(f,'flip_images.h5py'))
		time_stamps = list(F['right_image_flip']['ts'][:])
		assert(len(time_stamps)>0)
		ctr = 0
		for t in time_stamps:
			right_timestamp_index_dic[t] = ctr
			ctr += 1
			#print ctr
		F.close()
		print (len(right_timestamp_index_dic.values()),max(right_timestamp_index_dic.values()))
		so(right_timestamp_index_dic,opj(f,'right_timestamp_index_dic'))
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
#
##########################################









	#ctr += 1
	#if ctr > 1:
	#	break
all_aruco_left_timestamps = []
folders = sggo(data_path,'Aruco_Steering_Trajectories','*')
for f in folders:
	if car in f:
		try:
			o = lo(f)
			for r in o.keys():
				for b in o[r]:
					for t in o[r][b]:
						all_aruco_left_timestamps.append(t)
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)



#run_name,((t0,t0_index),bm,dire,steer,motor)


data_moments = []
files = sggo(data_path,'data_moments_*')
for f in files:
	o = lo(f)
	for i in rlen(o):
		o[i] = list(o[i])
	data_moments += o
so(opj(data_path,'data_moments'),data_moments)






###################################################


###################### left ####################
#
runs_left_timestamp_index_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	left_timestamp_index_dic = {}
	try:
		o=lo(opj(f,'left_timestamp_index_dic.pkl'))
		runs_left_timestamp_index_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
so(runs_left_timestamp_index_dic,opj(data_path,'runs_left_timestamp_index_dic'))
#
####################### right ##################
#
runs_right_timestamp_index_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	right_timestamp_index_dic = {}
	try:
		o=lo(opj(f,'right_timestamp_index_dic.pkl'))
		runs_right_timestamp_index_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
so(runs_right_timestamp_index_dic,opj(data_path,'runs_right_timestamp_index_dic'))
#
#################################################





runs_left_right_ts_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	try:
		o=lo(opj(f,'left_right_ts_dic.pkl'))
		runs_left_right_ts_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
so(runs_left_right_ts_dic,opj(data_path,'runs_left_right_ts_dic'))






################################3
#
runs_left_timestamp_index_dic = lo(opj(data_path,'runs_left_timestamp_index_dic.pkl'))
runs_right_timestamp_index_dic = lo(opj(data_path,'runs_right_timestamp_index_dic.pkl'))
data_moments = lo(opj(data_path,'data_moments.pkl'))
runs_left_right_ts_dic = lo(opj(data_path,'runs_left_right_ts_dic.pkl'))

ctr = 0
data_moments_indexed = []
for d in data_moments:
	try:
		n = d[0]
		t = d[1]
		i = runs_left_timestamp_index_dic[n][t]
		tr = runs_left_right_ts_dic[n][t]
		ir = runs_right_timestamp_index_dic[n][tr]
		data_moments_indexed.append([n,((t,i),(tr,ir)),(d[2],d[3]),(d[4],d[5])])
		ctr += 1
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
so(opj(data_path,'data_moments_indexed'),data_moments_indexed)
#
#################################



if False:
	All_image_files = {}
	#folders5 = sgg('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/*')
	for f in folders5:
		print fname(f)
		All_image_files[fname(f)] = {}
		if True:
			try:
				O = h5r(opj(f,'original_timestamp_data.h5py'))
				F = h5r(opj(f,'flip_images.h5py'))
				All_image_files[fname(f)]['normal'] = O
				All_image_files[fname(f)]['flip'] = F
			except Exception as e:
				print("********** Exception ***********************")
				print(e.message, e.args)	



	DIRECT = 'Direct_Arena_Potential_Field'
	FOLLOW = 'Follow_Arena_Potential_Field'
	CLOCKWISE = 0
	COUNTER_C = 1
	ctr = 0
	random.shuffle(data_moments_indexed)


	while(True):
		FLIP = random.choice([0,1])
		dm = data_moments_indexed[ctr]
		Data_moment = {}
		
		Data_moment['steer'] = zeros(90) + dm[3][0]
		if FLIP:
			Data_moment['steer'] = 99 - Data_moment['steer']
		Data_moment['motor'] = zeros(90) + dm[3][1]
		Data_moment['labels'] = {}
		for l in ['direct','follow','clockwise','counter-clockwise']:
			Data_moment['labels'][l] = 0
		Data_moment['name'] = dm[0]
		direction = dm[2][1]
		behavioral_mode = dm[2][0]
		if behavioral_mode == DIRECT:
			Data_moment['labels']['direct'] = 1
		elif behavioral_mode == FOLLOW:
			Data_moment['labels']['follow'] = 1

		if not FLIP:
			if direction == CLOCKWISE:
				Data_moment['labels']['clockwise'] = 1
			elif direction == COUNTER_C:
				Data_moment['labels']['counter-clockwise'] = 1
		else:
			if direction == COUNTER_C:
				Data_moment['labels']['clockwise'] = 1
			elif direction == CLOCKWISE:
				Data_moment['labels']['counter-clockwise'] = 1

		tl0 = dm[1][0][0]; il0 = dm[1][0][1]
		tr0 = dm[1][1][0]; ir0 = dm[1][1][1]

		if FLIP:
			F = All_image_files[Data_moment['name']]['flip']
		else:
			F = All_image_files[Data_moment['name']]['normal']

		Data_moment[left] = {}
		Data_moment[right] = {}

		if not FLIP:
			Data_moment[left][0] = F[left_image][vals][il0]
			Data_moment[right][0] = F[right_image][vals][ir0]
			Data_moment[left][1] = F[left_image][vals][il0+2] # note, two frames
			Data_moment[right][1] = F[right_image][vals][ir0+2]
		else:
			Data_moment[right][0] = F[left_image_flip][vals][il0]
			Data_moment[left][0] = F['right_image_flip'][vals][ir0]
			Data_moment[right][1] = F[left_image_flip][vals][il0+2]
			Data_moment[left][1] = F['right_image_flip'][vals][ir0+2]


		mi(Data_moment[left][0],'left0')
		mi(Data_moment[left][1],'left1')
		mi(Data_moment[right][0],'right0')
		mi(Data_moment[right][1],'right1')


		plt.title(d2s(FLIP,'motor',Data_moment['motor'][3],'steer',Data_moment['steer'][3]))
		spause();

		print Data_moment[labels]

		raw_enter()

		ctr += 1


		clf()

	#mi(l0,1)
	#mi(l0,2)














	car = 'Yellow'

	###################### left-right ts dic ####################
	#
	folders5 = sgg('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/*')
	for f in folders5:
		if car in f:
			try:
				F=h5r(opj(f,'original_timestamp_data.h5py'))
				print fname(f)
				r = F['right_image']['ts']
				l = F['left_image']['ts']
				left_right_dic = {}
				for i in range(len(l)):
					t = l[i]
					for j in range(max(0,i-10),min(i+10,len(r))):
						if r[j] > t and r[j] < t+0.1:
							left_right_dic[t] = r[j]
							break
				so(left_right_dic,opj(f,'left_right_ts_dic'))
			except Exception as e:
				print("********** Exception ***********************")
				print(e.message, e.args)			
				


















	Args = {'BATCH':'True'}
	if 'BATCH' in Args:
		if Args['BATCH'] == 'True':
			for color in ['Blue','Lt_Blue','Orange','Black','Yellow','Purple']:
				os.system(d2s("xterm -hold -e python",opjh('kzpy3/c/__temp.py'), 'CAR_NAME', 'Mr_'+color,'&'))
				pause(2)
			raw_enter();
			exit()
			assert(False)

	#EOF