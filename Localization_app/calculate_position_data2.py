#import kzpy3.Grapher_app.Graph_Image_Module as Graph_Image_Module
#import Parameters_Module
from Parameters_Module import *
#from vis2 import *


h5py_data_folder = Args['H5PY']

Observer = 'False'
if 'OBSERVER' in Args:
	if Args['OBSERVER'] == 'True':
		spd2s('OBSERVER')
		Observer = 'True'


if 'BATCH' in Args:
	if Args['BATCH'] == 'True':
		for the_car in P['CAR_LIST']:
			os.system(d2s("xterm -hold -fa monaco -fs 11 -e python kzpy3/Localization_app/calculate_position_data2.py CAR",the_car,"STEP",Args['STEP'],"OBSERVER",Observer,"H5PY",h5py_data_folder,'&'))
	#raw_enter();
	print('done!')
	exit()
	assert(False)
else:
	car = Args['CAR']


def get_car_position_heading_validity(h5py_data_folder,graphics=False):
	if len(gg(opj(h5py_data_folder,'left_timestamp_metadata_right_ts.h5py'))) > 0:
		L = h5r(opj(h5py_data_folder,'left_timestamp_metadata_right_ts.h5py'))
	else:
		L = h5r(opj(h5py_data_folder,'left_timestamp_metadata.h5py'))
	O = h5r(opj(h5py_data_folder,'original_timestamp_data.h5py'))
	A = h5r(opj(h5py_data_folder,'aruco_position.h5py'))
	if state in L:
		print len(A['aruco_position_y'][:]),len(L['state'][:])

	######################
	#
	ax = A[aruco_position_x][:]
	ay = A[aruco_position_y][:]
	hx = A[aruco_heading_x][:]
	hy = A[aruco_heading_y][:]
	heading_pause = A['heading_pause'][:]
	A_len = len(A[aruco_position_x][:])
	#ax = na(meo(na(L[aruco_position_x][:]),45))
	#ay = na(meo(na(L[aruco_position_y][:]),45))
	#hx = na(meo(na(L[aruco_heading_x][:]),45))
	#hy = na(meo(na(L[aruco_heading_y][:]),45))
	#
	###################### 

	left_images = O[left_image][vals][:].copy()
	left_images = left_images.mean(axis=3)
	right_images = O[right_image][vals][:].copy()
	right_images = right_images.mean(axis=3)


 
	n = [0]
	for i in range(1,A_len):#shape(left_images)[0]):
		if i < len(right_images):
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			mr = np.abs(right_images[i]-right_images[i-1]).mean()
			n.append((ml+mr)/2.0)
		else:
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			n.append(ml)			


	t = O[left_image][ts][:]


	hp = heading_pause
	#hp = L[heading_pause][:]
	hp[hp<1]=0
	hp2 = 1-hp
	if state in L:
		hp2[L[state][:A_len]!=6] = 0 # Ignoring human driving, not necessarily wanted for Smyth-Fernwald

	if False:
		mo_mask = L[motor][:A_len]*0.0+1.0 # in full_raised, motor signals not saved properly
		mo_mask[mo_mask<53]=0
		mo_mask[mo_mask>=53]=1.0
		o = mo_mask*hp2*n
	if True:
		o = hp2*n
	if Observer != 'True':
		if 'cmd_motor' in L:
			spd2s('cmd_motor is in L, assuming normal driving car (all zero anyway)')
			mo_mask = L['cmd_motor'][:A_len]*0.0+1.0
			mo_mask[mo_mask<53]=0 # these don't do anything because of above
			mo_mask[mo_mask>=53]=1.0
			o = mo_mask*hp2*n
		else:
			spd2s('cmd_motor is NOT in L, using motor but all zero anyway')
			mo_mask = L['motor'][:A_len]*0.0+1.0
			mo_mask[mo_mask<53]=0 # these don't do anything because of above
			mo_mask[mo_mask>=53]=1.0
			o = mo_mask*hp2*n
	else:
		pass
		#spd2s('Observer car')
		#o = na(hp)*0 + 1.0




	p=[]
	for q in o:
		if q > 0:
			p.append(q)
	

	o[o>(np.mean(p)+1.5*np.std(p))] = 0
	o[o<(np.mean(p)-1.5*np.std(p))] = 0
	
	
	o_meo = na(meo(o,45))
	

	pause_flag = False
                                     
	L.close()
	O.close()
	A.close()
	return t,ax,ay,hx,hy,o_meo



if Args['STEP'] == 'position_data':

	#for car in ['Mr_Orange','Mr_Lt_Blue','Mr_Blue','Mr_Yellow','Mr_Black','Mr_Purple']:
	#h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo_2/h5py'
	#print opj(h5py_data_folder,car+'*')
	runs = []
	if False:
		runs = sggo(h5py_data_folder,car+'*')
	else: # NOTE!!!! THIS WILL FAIL FOR NAMES LIKE Mr_Silver_Orange
		spd2s('NOTE!!!! THIS WILL FAIL FOR NAMES LIKE Mr_Silver_Orange')
		all_runs_ = sggo(h5py_data_folder,'*')
		for r in all_runs_:
			if car in r:
				runs.append(r)
	print runs
	for r in runs:
		print 'processing '+r
		
		if len(sggo(r,'position_data.h5py')) > 0:
			unix_str = 'rm '+opj(r,'position_data.h5py')
			print(unix_str)
			unix(unix_str,False)
			#print opj(r,'position_data.h5py') + 'exists, doing nothing'
		#else:
		if True:
			
			if True:#try:
				t,ax,ay,hx,hy,o_meo = get_car_position_heading_validity(r,graphics=False)

				F = h5w(opj(r,'position_data.h5py'))
				F.create_dataset('t',data=t)
				F.create_dataset('ax',data=ax)
				F.create_dataset('ay',data=ay)
				F.create_dataset('hx',data=hx)
				F.create_dataset('hy',data=hy)
				F.create_dataset('o_meo',data=o_meo)
				F.close()
			else:#except Exception as e:
				print("********** calculate_position_data.py: Exception ***********************")
				print(e.message, e.args)
				raw_enter()


elif Args['STEP'] == 'position_dictionaries':

	#for car in ['Mr_Orange','Mr_Lt_Blue','Mr_Blue','Mr_Yellow','Mr_Black','Mr_Purple']:

	#h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo_2/h5py'

	runs = []
	if False:
		runs = sggo(h5py_data_folder,car+'*')
	else:
		spd2s('NOTE!!!! THIS WILL FAIL FOR NAMES LIKE Mr_Silver_Orange')
		all_runs_ = sggo(h5py_data_folder,'*')
		for r in all_runs_:
			if car in r:
				runs.append(r)
	print runs

	All_100ms_data = {}
	for topic in ['ax','ay','hx','hy','o_meo']:
		All_100ms_data[topic] = {}
	for r in runs:
		print r
		Data_100ms = {}
		if len(sggo(r,'position_data.h5py')) > 0:
			F = h5r(opj(r,'position_data.h5py'))
			TS_100ms = {}
			for t in F['t']:
				TS_100ms[dp(t,1)] = True
			Data_100ms['t'] = sorted(TS_100ms.keys())
			for topic in ['ax','ay','hx','hy','o_meo']:
				print topic, len(Data_100ms['t']),len(F['t'][:]),len(F[topic][:])
				Data_100ms[topic] = np.interp(Data_100ms['t'],F['t'][:len(F[topic][:])],F[topic][:])
			for topic in ['ax','ay','hx','hy','o_meo']:
				for i in rlen(Data_100ms[topic]):
					All_100ms_data[topic][Data_100ms['t'][i]] = Data_100ms[topic][i]
			F.close()
	unix('mkdir -p '+opj(pname(h5py_data_folder),'position_dictionaries'))
	so(opj(pname(h5py_data_folder),'position_dictionaries',car+'_position_dictionary'),All_100ms_data)
	


print('Done!')

#EOF
