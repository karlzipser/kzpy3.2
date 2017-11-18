from kzpy3.Grapher_app.Graph_Image_Module import *

h5py_data_folder = Args['H5PY']

if 'BATCH' in Args:
	if Args['BATCH'] == 'True':
		for color in ['Blue','Lt_Blue','Orange','Black','Yellow','Purple']:
			os.system(d2s("xterm -hold -e python kzpy3/Localization_app/calculate_position_data2.py CAR Mr_"+color,"H5PY",h5py_data_folder,'&'))
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
	print len(L['aruco_position_y'][:])
	left_images = O[left_image][vals][:].copy()
	left_images = left_images.mean(axis=3)
	right_images = O[right_image][vals][:].copy()
	right_images = right_images.mean(axis=3)


 
	n = [0]
	for i in range(1,shape(left_images)[0]):
		if i < len(right_images):
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			mr = np.abs(right_images[i]-right_images[i-1]).mean()
			n.append((ml+mr)/2.0)
		else:
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			n.append(ml)			


	t = O[left_image][ts][:]



	hp = L[heading_pause][:]
	hp[hp<1]=0
	hp2 = 1-hp
	hp2[L[state][:]!=6] = 0

	mo_mask = L[motor][:]
	mo_mask[mo_mask<53]=0
	mo_mask[mo_mask>=53]=1.0
	o = mo_mask*hp2*n


	p=[]
	for q in o:
		if q > 0:
			p.append(q)
	

	o[o>(np.mean(p)+1.5*np.std(p))] = 0
	o[o<(np.mean(p)-1.5*np.std(p))] = 0
	
	
	o_meo = na(meo(o,45))
	

	pause_flag = False

	ax = na(meo(na(L[aruco_position_x][:]),45))
	ay = na(meo(na(L[aruco_position_y][:]),45))
	hx = na(meo(na(L[aruco_heading_x][:]),45))
	hy = na(meo(na(L[aruco_heading_y][:]),45))

	L.close()
	O.close()

	return t,ax,ay,hx,hy,o_meo



if True:

	#for car in ['Mr_Orange','Mr_Lt_Blue','Mr_Blue','Mr_Yellow','Mr_Black','Mr_Purple']:
	#h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo_2/h5py'
	print opj(h5py_data_folder,car+'*')
	runs = sggo(h5py_data_folder,car+'*')

	for r in runs:
		print r
		
		if len(sggo(r,'position_data.h5py')) > 0:
			unix('rm '+opj(r,'position_data.h5py'))
			#print opj(r,'position_data.h5py') + 'exists, doing nothing'
		#else:
		if True:
			print 'processing '+r
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


if False:

	#for car in ['Mr_Orange','Mr_Lt_Blue','Mr_Blue','Mr_Yellow','Mr_Black','Mr_Purple']:

	#h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo_2/h5py'

	runs = sggo(h5py_data_folder,car+'*')
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
				Data_100ms[topic] = np.interp(Data_100ms['t'],F['t'][:],F[topic][:])
			for topic in ['ax','ay','hx','hy','o_meo']:
				for i in rlen(Data_100ms[topic]):
					All_100ms_data[topic][Data_100ms['t'][i]] = Data_100ms[topic][i]
			F.close()
	so(opj(pname(h5py_data_folder),car+'_position_dictionary'),All_100ms_data)
	


print('Done!')

#EOF
