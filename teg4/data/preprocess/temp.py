from kzpy3.teg3.data.preprocess.preprocess_bag_data import *

bfp = '/media/karlzipser/rosbags/direct_home_06Dec16_16h01m42s_Mr_Blue'

preprocess_bag_data(bfp,[]);

L=load_obj('/home/karlzipser/Desktop/direct_home_06Dec16_16h01m42s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')

if False:
	ts = sorted(L.keys())
	dts = [0]
	for i in range(1,len(ts)):
		dts.append(ts[i] - ts[i-1])
	figure(1)
	plot(ts,dts)
	figure(2)
	hist(dts)

import kzpy3.teg3.data.access.Bag_Folder as Bag_Folder
import kzpy3.teg3.data.access.Bag_File as Bag_File

BF = Bag_Folder.init('/home/karlzipser/Desktop/direct_home_06Dec16_16h01m42s_Mr_Blue',
	preprocessed_dir='.preprocessed2',
	left_image_bound_to_data_name='left_image_bound_to_data.pkl',
	NUM_STATE_ONE_STEPS=10)



#plot(BF['data']['raw_timestamps'],BF['data']['state_one_steps'],'bo-')
plot(BF['data']['good_start_timestamps'],zeros(len(BF['data']['good_start_timestamps']))+100,'go')
#plot(BF['data']['raw_timestamps'],2000*np.array(BF['data']['raw_timestamp_deltas']),'r')
#plot(BF['data']['raw_timestamps'],100*BF['data']['encoder'],'r')
#plot(BF['data']['raw_timestamps'],100*BF['data']['state'],'r')
#plot(BF['data']['raw_timestamps'],100*BF['data']['acc_z'],'r')

bf = BF['bag_file_num_dic'][15]  
bid = Bag_File.load_images(bf)
bag_left_timestamps = sorted(bid['left'].keys())
plot(bag_left_timestamps,2000+np.zeros(bag_left_timestamps),'go')

good_bag_timestamps = list(set(BF['data']['good_start_timestamps']) & set(bag_left_timestamps))
plot(good_bag_timestamps,2000+np.zeros(len(good_bag_timestamps)),'ro')


ts = sorted(bid['left'].keys())
for t in ts:
	mi(bid['left'][t],'left')
	#mi(bid['right'][BF['left_image_bound_to_data'][t]['right_image']],'right')
	plt.pause(0.0001)

plot(BF['data']['steer'],BF['data']['gyro_y'],'o')

"""
L=load_obj('/media/karlzipser/bair_car_data_7/rosbags14/direct_racing_Tilden_27Nov16_10h41m05s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')
ts = sorted(L.keys())
dts = [0]
for i in range(1,len(ts)):
	dts.append(ts[i] - ts[i-1])
figure(3)
plot(ts,dts)
figure(4)
hist(dts)

"""

pass



if False:
	bf = random.choice(BF['bag_file_num_dic'])
	bid = Bag_File.load_images(bf)
	bag_left_timestamps = sorted(bid['left'].keys())
	plot(bag_left_timestamps,2000+np.zeros(len(bag_left_timestamps)),'go')

	good_bag_timestamps = list(set(BF['data']['good_start_timestamps']) & set(bag_left_timestamps))
	plot(good_bag_timestamps,2000+np.zeros(len(good_bag_timestamps)),'ro')

	ts = sorted(bid['left'].keys())
	for t in ts:
		mi(bid['left'][t],'left')
		#mi(bid['right'][BF['left_image_bound_to_data'][t]['right_image']],'right')
		plt.pause(0.0001)



import cv2
a = np.random.rand(376,672,3)
a = 255*a
b=a.astype(np.uint8)

t0 = time.time()
for i in range(1000):
	c = imresize(b,25)
t1 = time.time()
print shape(c)
mi(c,'imresize')

t2 = time.time()
for i in range(1000):
	d = cv2.resize(b,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
t3 = time.time()
mi(d,'cv2.resize')
print shape(d)
print(t1-t0,t3-t2)


import cv2
a = np.random.rand(376,672,3)
a = 255*a
b=a.astype(np.uint8)

t0 = time.time()
for i in range(1000):
	c = scipy.fliplr(b)
t1 = time.time()
print shape(c)
mi(c,'fliplr')

t2 = time.time()
for i in range(1000):
	d = cv2.flip(b,1)
t3 = time.time()
mi(d,'cv2.flip')
print shape(d)
print(t1-t0,t3-t2)


import kzpy3.teg4.data.access.Bag_File as Bag_File 
bid = Bag_File.load_images('/home/karlzipser/Desktop/bair_car_data_rgb_1to4/direct_2Sept2016_Mr_Orange_to_Evans_and_back_2/bair_car_2016-09-02-11-52-00_36.bag.pkl' )

l = a_key(bid['left'])
li = bid['left'][l]
lf = bid['left_flip'][l]
r = a_key(bid['left'])
ri = bid['left'][r]
rf = bid['left_flip'][r]
mi(li,1,[2,2,1],do_clf=False)
mi(lf,1,[2,2,2],do_clf=False)
mi(ri,1,[2,2,3],do_clf=False)
mi(rf,1,[2,2,4],do_clf=False)




l=load_obj('/home/karlzipser/Desktop/loss.pkl' )
l2 = []
t2 = []
ctr = 0
a = 0
for i in range(len(l)):
	a += l[i]
	ctr += 1
	if ctr > 1000:
		l2.append(a/(1.*ctr))
		t2.append(i)
		a = 0
		ctr = 0
figure(1)
clf()
#plot(l)
plot(t2,l2,'ro-')

