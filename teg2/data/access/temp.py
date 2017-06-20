if False:

	from kzpy3.teg2.data.access.get_data_from_bag_files6 import * 
	#B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_28Sep16_08h06m57s_Mr_Orange'  )
	B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_4_min/caffe_z2_direct_local_Tilden_22Sep16_14h31m11s_Mr_Orange')
	data = 'timecourse data'
	plt.figure(data);plt.clf()
	ts = B.data['timestamps']
	plt.figure(data);
	topics = sorted(B.data.keys())

	ctr = 6.0
	legend_handles = []
	for tp in topics:
		if tp != 'timestamps':
			legend_handles.append(z2o_plot(ts,B.data[tp],ctr,'.',tp)[0])
			ctr -= 0.5
	plt.legend(handles=legend_handles)

	plt.figure('scatter')
	b=B.data['state_one_steps']
	plt.plot(B.data['steer'][b>0],B.data['gyro_x'][b>0],'.')





	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BCD = Bair_Car_Data(opjD('bair_car_data_min'),['caffe','play','follow','Tilden','Aug','Sep'])

	for i in range(7):
		t0 = time.time()
		print d2s("*************** i =",i,"*************************")
		BCD.load_bag_folder_images(250./(30./1000.))
		print d2s("time =",time.time()-t0)

	 

	N=30
	while True:
		bf=an_element(BCD.bag_folders_dic)
		if bf.data['acc_z'].mean() > 5: # the mean should be around 9.5 if acc is in datafile
			break
	indx = random.randint(0,len(bf.data['state_one_steps_1s_indicies'])-1)
	topics = ['steer_z_scored','motor_z_scored','acc_x_z_scored','acc_y_z_scored','acc_z_z_scored','gyro_x_z_scored','gyro_y_z_scored','gyro_z_z_scored',]
	data = []
	target = []
	target2 = []
	for tp in topics:
		zero_topic = False
		if random.random() < 0.2:
			zero_topic = True
		for i in range(N):
			d = bf.data[tp][indx+i]
			target.append(d)
			if i == N-1:
				target2.append(d)
			if zero_topic:
				d *= 0
			data.append(d)
	plt.plot(data)
	plt.plot(target)


	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BF = Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_02Oct16_15h53m07s_Mr_Orange' )
	BF.load_all_bag_files()
	dd = BF.get_data()

	t0 = time.time()
	for i in range(1000):
		q = an_element(BF.left_image_bound_to_data)
		#dd = BF.get_data()
	print(time.time()-t0)



	from kzpy3.teg2.data.access.get_data_from_bag_files6 import *
	BCD = Bair_Car_Data(opjD('bair_car_data_min'),['play','follow','Tilden','Aug','Sep']) #'campus','caffe'

	BCD.load_bag_folder_images(250./(30./1000.))

	plt.ion()

	t_start()
	for i in range(100000):
		print i
		#try:
		#BF = BCD.bag_folders_dic[a_key(BCD.bag_folders_with_loaded_images)]
		#if len(BF.img_dic['left'])==0:
		#	print "**************** BF.load_all_bag_files() *************"
		#	BF.load_all_bag_files()
		data_dic = BCD.get_data()
		#if np.mod(i,100) == 0:
		#	mi(data_dic['left'])
		#	plt.pause(0.001)
		#except Exception as e:
		#	print d2s("BF.path =,",BF.path,",i =",i,"len(BF.img_dic['left']) = ",len(BF.img_dic['left']))
		#	print e.message, e.args
		#	break
	t_end()



	def get_data(BCD,topics=['steer','motor'],num_topic_steps=10,num_image_steps=2,state_one_steps_indicies_str='state_one_steps_0_5s_indicies'):
		BF = BCD.bag_folders_dic[a_key(BCD.bag_folders_with_loaded_images)]
		return BF.get_data(topics,num_topic_steps,num_image_steps,state_one_steps_indicies_str)





	no_left_ts = []
	for i in range(len(BF.data['timestamps'])):
		t = BF.data['timestamps'][i]
		if np.mod(i,1000)==0:
			print i
		if t not in BF.img_dic['left'].keys():
			print d2s(BF.path,t)
			no_left_ts.append(t)

	plt.figure(1)
	plt.clf()
	plt.plot(a,'o')
	plt.plot(b,'o')


if True:
	from kzpy3.teg2.data.access.get_data_from_bag_files7 import *
	path = opjD('bair_car_data_min/direct_local_sidewalks_27Sep16_16h45m54s_Mr_Orange')# 'bair_car_data_min/play_30Aug2016_Mr_Blue_Tilden_1') #'bair_car_data_min/direct_campus_25Sep16_09h34m37s_Mr_Orange')
	BF=Bag_Folder(path)

	t_start()
	for i in range(100000):
		d=BF.get_data()
		#BF.verify_get_data(d)
	t_end()





from kzpy3.teg2.data.access.get_data_from_bag_files8 import *
f = random.choice(gg(opjD('bair_car_data_min','*')))
f='/home/karlzipser/Desktop/bair_car_data_min/furtive_9August2016'

N_topics = 10
N_frames = N_topics; assert(N_topics >= N_frames)
BF=Bag_Folder(f,N_topics)

t_start()
for i in range(1000):
	d = BF.get_data(['state','steer','motor','encoder','gyro_x','gyro_y','gyro_z','acc_x','acc_y','acc_z'],N_topics,N_frames)
	show_data_dic(d)
	#print "<pause>"
	#plt.pause(0.1)
	plt.title('<pause>')
	BF.incremental_index += N_frames
t_end()

n=10
plt.figure(n)
plt.clf()
mi(d['left'][0],n,[2,2,2],do_clf=False)
mi(d['left'][1],n,[2,2,4],do_clf=False)
mi(d['right'][1],n,[2,2,3],do_clf=False)
mi(d['right'][0],n,[2,2,1],do_clf=False)






from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
path = '/home/karlzipser/Desktop/bair_car_data_min/play_Nino_to_campus_08Oct16_09h00m00s_Mr_Blue_1c'
list0 = []
list1 = ['play','follow','furtive','caffe','direct_from_campus2_08Oct16_10h15m','direct_from_campus_31Dec12_10h00m','direct_to_campus_08Oct16_08h55m37']
#list2 = ['Tilden','play','follow','furtive','play','follow','furtive','caffe','local','Aug','Sep']
list3 = ['direct','caffe','play','follow']
bair_car_data_path = opjD('bair_car_data_min')#'/media/ExtraDrive1/bair_car_data_min'
bair_car_data = Bair_Car_Data(bair_car_data_path,list3)



bf = random.choice(bair_car_data.bag_folders_weighted)
BF = bair_car_data.bag_folders_dic[bf]
BF.path
show_data_dic_sequence(BF)



	self.steer_angle_dic = {}
	for i in range(len(self.data['steer'])):
		steer = self.data['steer'][i]
		steer = int(steer)
		if steer < 0:
			steer = 0
		if steer > 99:
			steer = 99
		if not steer in self.steer_angle_dic:
			self.steer_angle_dic[steer] = []
		self.steer_angle_dic[steer].append(i)
 


	def get_random_steer_equal_weighting(self):
		indx = -99
		steer = np.random.randint(0,100)
		if steer in steer_angle_dic:
			indx = random.choice(steer_angle_dic[steer])
			break
		assert(indx >= 0)
		return indx

from kzpy3.teg2.data.access.get_data_from_bag_files9 import *
bair_car_data_path = opjD('bair_car_data_min')
bair_car_data = Bair_Car_Data_temp(bair_car_data_path,[])


















d=[[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -30, -30, -30, -30],
	[ 11, 9, 6, 12, 11, 16, 23, 21, 23,  14, 20, 29, 26, 32, 31, 36, 40, 35]]

d=[[24, 36, 54, 64, 71, 83, 92, 84,  0, -58, -60, -60, -60, -60, -34, -25, 0],
	[20, 22, 29, 39, 43, 50, 56, 65,  -2, 7, 9, 8, 8, 13, 8, 12, 12]]

[ 10, 27, 51, 87, 90, 90, 112, 114, 120, 14, -30, -60, -60, -60, -60, -60, -60, -60, -90]
[2, 9, 11, 12, 19, 23, 25, 30, 34, 18, -6, -10, -18, -18, -23, -24, -28, -29, -29]

[ 7, 40, 50, 50, 76, 80, 89, 99, 112, 3, 79, 178, 122, 82, 45, -19, -30, -30, -30]
[ -11, -16, -12, -18, -15, -16, -12, -9, -16, 1, 10, 14, 21, 26, 27, 30, 29, 36, 39]












#!/usr/bin/env python
"""
reed to run roslaunch first, e.g.,

roslaunch bair_car bair_car.launch use_zed:=true record:=false
"""

########################################################
#          CAFFE SETUP SECTION
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()
from kzpy3.utils import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files2 import *
import cv2
os.chdir(home_path) # this is for the sake of the train_val.prototxt

solver_file_path = opjh("kzpy3/caf3/z2/solver_live.prototxt")
weights_file_path = opjD('z2/z2.caffemodel') #
def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver
#solver = setup_solver()
#if weights_file_path != None:
#	print "loading " + weights_file_path
#	solver.net.copy_from(weights_file_path)
#
########################################################






#G = load_obj(opjD('good_start_timestamp_indicies_test_results'))
k_code = {}
L = {}
l_all = []
plt.ion()
ctr = 0
for k in G:
	k_code[ctr] = k
	print fn(k)

	a = G[k]
	l = a['loss']
	l_all += l
	l = np.array(l)
	print d2s("errors: ",len(l[l<0]),"in",len(l))
	l[l<0] = 0
	hist(l)
	plt.title(fn(k))
	plt.xlim((0,1))
	plt.pause(0.005)
	for i in range(len(l)):
		m = l[i]
		m *= 100
		m = to_range(m,0,60)
		m = int(m)
		if not m in L:
			L[m] = []
		L[m].append((ctr,i))
	ctr += 1
	#raw_input('enter to contine')




l_all = np.array(l_all)
l_all[l_all<0] = 0
hist(l_all)

gt20 = 0
le20 = 0
for i in range(61):
	if i in L:
		if i <= 23:
			le20 += len(L[i])
		else:
			gt20 += len(L[i])
print le20,gt20,np.round(100*gt20/(1.0*le20+gt20))

ctr = 0
for i in range(len(l_all)):
	if l_all[i] <= 0.23:
		ctr += 1
print (ctr,len(l_all)-ctr,len(l_all))

def make_loss_indicies_dic():
	global good_start_timestamp_indicies_test_results
	a = good_start_timestamp_indicies_test_results[self.path]
	l = a['loss']
	l = np.array(l)
	l[l<0] = 0
	for i in range(len(l)):
		m = l[i]
		m *= 100
		m = to_range(m,0,60)
		m = int(m)
		if not m in self.loss_indicies_dic:
			self.loss_indicies_dic[m] = []
		self.loss_indicies_dic[m].append((ctr,i))
	ctr += 1
	#raw_input('enter to contine')



from kzpy3.vis import *
MLK_pm_lat = 37.881556
MLK_pm_lon = -122.278434
miles_per_deg_lat = 68.94
miles_per_deg_lon_at_37p88 = 54.41
meters_per_mile = 1609.34
b=load_obj('/home/karlzipser/Desktop/temp_bag/caffe_z2_direct_local_sidewalk_test_data_03Nov16_18h33m09s_Mr_Orange/.preprocessed/left_image_bound_to_data3.pkl' )


ts = sorted(b.keys())

topics = ['gyro_heading_x','gyro_heading_y','gyro_heading_z',
'gyro_x','gyro_y','gyro_z',
'GPS2_lat','GPS2_long','GPS2_speed','GPS2_angle',
'motor','steer','encoder',
'acc_x','acc_y','acc_z','state']

Data = {}
for tp in topics:
	Data[tp] = []

for t in ts:                                                                   
	Data['gyro_heading_x'].append(b[t]['gyro_heading'][0])
	Data['gyro_heading_y'].append(b[t]['gyro_heading'][1])
	Data['gyro_heading_z'].append(b[t]['gyro_heading'][2])
	Data['GPS2_lat'].append(b[t]['GPS2_lat'])
	Data['GPS2_long'].append(b[t]['GPS2_long'])
	Data['GPS2_speed'].append(b[t]['GPS2_speed'])
	Data['motor'].append(b[t]['motor'])
	Data['steer'].append(b[t]['steer'])
	Data['encoder'].append(b[t]['encoder'])
	Data['acc_x'].append(b[t]['acc'][0])
	Data['acc_y'].append(b[t]['acc'][1])
	Data['acc_z'].append(b[t]['acc'][2])
	Data['gyro_x'].append(b[t]['gyro'][0])
	Data['gyro_y'].append(b[t]['gyro'][1])
	Data['gyro_z'].append(b[t]['gyro'][2])
	Data['state'].append(b[t]['state'])

for tp in topics:
	Data[tp] = na(Data[tp])

Data['meters_y'] = (Data['GPS2_lat']-MLK_pm_lat)*miles_per_deg_lat*meters_per_mile
Data['meters_x'] = (Data['GPS2_long']-MLK_pm_lon)*miles_per_deg_lon_at_37p88*meters_per_mile

hx = Data['gyro_heading_x']
hy = Data['gyro_heading_y']
hz = Data['gyro_heading_z']
hdx=0*hx;hdy=0*hy;hdz=0*hz
for i in range(1+5*30,len(hx),1):
    hdx[i] =  hx[i]-hx[(i-5*30):(i-4*30)].mean()
    hdy[i] =  hy[i]-hy[(i-5*30):(i-4*30)].mean()
    hdz[i] =  hz[i]-hz[(i-5*30):(i-4*30)].mean()
Data['d_gyro_heading_x'] = hdx
Data['d_gyro_heading_y'] = hdy
Data['d_gyro_heading_z'] = hdz


zData = {}
for tp in ['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',
	'd_gyro_heading_x','d_gyro_heading_y','d_gyro_heading_z']:
	zData[tp] = zscore(Data[tp],3)
zData['meters_x'] = Data['meters_x']/10.0
zData['meters_y'] = Data['meters_y']/10.0
zData['state'] = Data['state'].copy()
for i in range(len(zData['state'])):
	if int(zData['state'][i]) in [5,7]:
		zData['state'][i] = 1
	else:
		zData['state'][i] = 0
zData['motor'] = (Data['motor']-49.)/10.
zData['steer'] = zscore(Data['steer'],3)
zData['encoder'] = Data['encoder']/3.





img = zeros((len(zData.keys()),len(zData['state'])))
topics = sorted(zData.keys())
ctr = 0
for tp in topics:
	img[ctr,:] = zData[tp]
	ctr += 1

for i in range(20000,60000,2):
	input_img = img[:,i-150:i]
	mi(input_img)
	plt.pause(0.001)
	steer_target = []
	motor_target = []
	for j in range(i,i+10):
		if zData['state'][j] == 1:
			steer_target.append(int(Data['steer'][j]))
			motor_target.append(int(Data['motor'][j]))
		else:
			steer_target.append(49)
			motor_target.append(49)
	print steer_target
	print motor_target
	print "---"






"""
['acc_x',
 'acc_y',
 'acc_z',
 'd_gyro_heading_x',
 'd_gyro_heading_y',
 'd_gyro_heading_z',
 'encoder',
 'gyro_x',
 'gyro_y',
 'gyro_z',
 'meters_x',
 'meters_y',
 'motor',
 'state',
 'steer']
"""


def gps_plotter(start,stop,lat,lon,lat_orig=MLK_pm_lat,lon_orig=MLK_pm_lon,d_lat=0.0005,d_lon=0.0005,d_meters=100):
	lat = na(lat[start:stop])
	lon = na(lon[start:stop])
	d_lat = na(d_lat)
	d_lon = na(d_lon)
	lat_meters_from_orig = (lat-lat_orig)*miles_per_deg_lat*meters_per_mile
	lon_meters_from_orig = (lon-lon_orig)*miles_per_deg_lon_at_37p88*meters_per_mile
	
	plt.figure(1)
	plt.clf()
	plt.plot(lon,lat,'o')
	plt.ylim(lat_orig-d_lat/2.,lat_orig+d_lat/2.)
	plt.xlim(lon_orig-d_lon/2.,lon_orig+d_lon/2.)
	plt_square()

	
	plt.figure(2)
	plt.clf()
	plt.plot(lon_meters_from_orig,lat_meters_from_orig,'o')
	plt.ylim(-d_meters/2.,+d_meters/2.)
	plt.xlim(-d_meters/2.,+d_meters/2.)
	plt_square()



gps_plotter(20000,60000,gx,gy)