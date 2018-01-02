from kzpy3.utils2 import *
from Parameters_Module import *
data_path = Args['PATH']





###################### left-right ts dic ####################
#
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	if True:#car in f:
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
			print("********** Exception 1 ***********************")
			print(e.message, e.args)



##################################################################################
#
folders5 = sggo(data_path,'h5py','*')
all_left_timestamps = []
for car in P['CAR_LIST']:
	for f in folders5:
		if car in f:
			print f
			all_left_timestamps = []			
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
				print("********** Exception 11 ***********************")
				print(e.message, e.args)

	common_timestamps = sorted(list(set(all_left_timestamps) & set(all_aruco_left_timestamps)))
	valid_timestamps = []
	valid_timestamp_pairs = {}
	for i in range(0,len(common_timestamps)-1):
		if common_timestamps[i+1] - common_timestamps[i] < 1/30.*3.0:
			valid_timestamps.append(common_timestamps[i])
			valid_timestamp_pairs[common_timestamps[i]] = common_timestamps[i+1]
	unix(d2s('mkdir',opj(data_path,'support')),False,False,False)
	so(opj(data_path,'support','valid_timestamps.'+car+'.pkl'),valid_timestamps)
	so(opj(data_path,'support','valid_timestamp_pairs.'+car+'.pkl'),valid_timestamp_pairs)



	valid_timestamps = lo(opj(data_path,'support','valid_timestamps.'+car+'.pkl'))
	data_moments = []
	folders = sggo(data_path,'Aruco_Steering_Trajectories','*')
	invalid_t = 0
	ts_number = 0
	for f in folders:
		print(f+' in folders')
		try:
			run_name = fname(f).split('.')[0]
			if car in run_name:
				o = lo(f)
				for r in o.keys(): # behavioral mode
					for b in o[r]: # clockwise/counter clockwise
						for t in o[r][b]: # timestamp
							ts_number += 1
							if t in valid_timestamps:
								steer = o[r][b][t]['steer']
								motor = o[r][b][t]['motor']
								other_car_in_view = o[r][b][t]['other_car_in_view']
								data_moments.append((run_name,t,r,b,steer,motor,other_car_in_view))
								#print data_moments[-1]
							else:
								#print t,'invalid'
								invalid_t += 1
		except Exception as e:
			print("********** Exception 10 ***********************")
			print(e.message, e.args)
	so(data_moments,opj(data_path,'support','data_moments_'+car))
	try:
		spd2s('percent invalid =',dp(invalid_t/(1.0*ts_number)*100.0,1))
	except Exception as e:
		print("********** q Exception ***********************")
		print(e.message, e.args)	
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
		print("********** Exception 9 ***********************")
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
		print("********** Exception 8***********************")
		print(e.message, e.args)
#
##########################################










all_aruco_left_timestamps = []
folders = sggo(data_path,'Aruco_Steering_Trajectories','*')
for f in folders:
	print f
	for car in P['CAR_LIST']:
		if car in f:
			print car
			try:
				o = lo(f)
				for r in o.keys():
					for b in o[r]:
						for t in o[r][b]:
							all_aruco_left_timestamps.append(t)
				print 'okay'
			except Exception as e:
				print("********** Exception 7 ***********************")
				print(e.message, e.args)



#run_name,((t0,t0_index),bm,dire,steer,motor)


data_moments = []
files = sggo(data_path,'support','data_moments_*')
for f in files:
	o = lo(f)
	for i in rlen(o):
		o[i] = list(o[i])
	data_moments += o
so(opj(data_path,'support','data_moments'),data_moments)






###################################################


###################### left ####################
#
print('left')
runs_left_timestamp_index_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	left_timestamp_index_dic = {}
	try:
		o=lo(opj(f,'left_timestamp_index_dic.pkl'))
		runs_left_timestamp_index_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception 6 ***********************")
		print(e.message, e.args)
so(runs_left_timestamp_index_dic,opj(data_path,'support','runs_left_timestamp_index_dic'))
#
####################### right ##################
#
print('right')
runs_right_timestamp_index_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	right_timestamp_index_dic = {}
	try:
		o=lo(opj(f,'right_timestamp_index_dic.pkl'))
		runs_right_timestamp_index_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception 5 ***********************")
		print(e.message, e.args)
so(runs_right_timestamp_index_dic,opj(data_path,'support','runs_right_timestamp_index_dic'))
#
#################################################




print('runs_left_right_ts_dic')
runs_left_right_ts_dic = {}
folders5 = sggo(data_path,'h5py','*')
for f in folders5:
	print fname(f)
	try:
		o=lo(opj(f,'left_right_ts_dic.pkl'))
		runs_left_right_ts_dic[fname(f)] = o
	except Exception as e:
		print("********** Exception 4 ***********************")
		print(e.message, e.args)
so(runs_left_right_ts_dic,opj(data_path,'support','runs_left_right_ts_dic'))






################################3
#
print('data_moments_indexed')
runs_left_timestamp_index_dic = lo(opj(data_path,'support','runs_left_timestamp_index_dic.pkl'))
runs_right_timestamp_index_dic = lo(opj(data_path,'support','runs_right_timestamp_index_dic.pkl'))
data_moments = lo(opj(data_path,'support','data_moments.pkl'))
runs_left_right_ts_dic = lo(opj(data_path,'support','runs_left_right_ts_dic.pkl'))

ctr = 0
data_moments_indexed = []
for d in data_moments:
	#print d
	try:
		#print d
		n = d[0] #run_name
		t = d[1] # timestamp
		i = runs_left_timestamp_index_dic[n][t]
		tr = runs_left_right_ts_dic[n][t]
		ir = runs_right_timestamp_index_dic[n][tr]
		data_moments_indexed.append({'run_name':n,'left_ts_index':(t,i),'right_ts_index':(tr,ir),'behavioral_mode':d[2],'counter_clockwise':d[3],'steer':d[4],'motor':d[5],'other_car_in_view':d[6]})
		ctr += 1
	except Exception as e:
		print("********** Exception 3 ***********************")
		print(e.message, e.args)
		print ctr
so(opj(data_path,'data_moments_indexed'),data_moments_indexed)
#
#################################


spd2s('Done with',data_path)