# python
# model cars
# data aruco


###########
#
def Image(xyz_sizes,origin,mult,data_type=np.uint8):
	D = {}
	D['origin'] = origin
	D['mult'] = mult
	D['Purpose'] = 'An image which translates from float coordinates.'
	D['floats_to_pixels'] = _floats_to_pixels
	if len(xyz_sizes) == 2:
		D['img'] = zeros((xyz_sizes[0],xyz_sizes[1]),data_type)
	elif len(xyz_sizes) == 2:
		D['img'] = zeros((xyz_sizes[0],xyz_sizes[1],xyz_sizes[2]),data_type)
	else:
		assert(False)
	return D

def _floats_to_pixels(D,xy):
	xy = array(xy)
	xy[:,0] *= -D['mult']
	xy[:,0] += D['origin']
	xy[:,1] *= D['mult']
	xy[:,1] += D['origin']
	return xy


#
###############


###############
#
def Markers(markers_clockwise,radius):
	D = {}
	D['clockwise'] = markers_clockwise
	D['ids_all'] = []
	D['angles_dic'] = {}
	D['angles'] = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
	D['xy'] = []
	for i in range(len(markers_clockwise)):
		a = D['angles'][i]
		D['angles_dic'][markers_clockwise[i]] = a
		x = radius*np.sin(a)
		y = radius*np.cos(a)
		D['xy'].append([x,y])
	D['xy_dic'] = {}
	assert(len(markers_clockwise) == len(D['xy']))
	D['cv2_draw'] = _cv2_draw
	return D

def _cv2_draw(D,img):
	for j in range(len(D['clockwise'])):
		m = D['clockwise'][j]
		xy = D['xy'][j]
		D['xy_dic'][m] = xy
		c = (255,0,0)
		xp,yp = img['floats_to_pixels'](xy)
		cv2.circle(img['img'],(xp,yp),4,c,-1)


#
###################

markers = Markers(range(96),4*107/100.)

Origin = 300
Mult = 50

img = Image([Origin*2,Origin*2],Origin,Mult)

markers['cv2_draw'](markers,img)






def pretty(d, indent=0):
	ctr = 0
	for key, value in d.iteritems():
		if ctr < 4:
			print '\t' * indent + str(key)
		elif ctr == 4:
			print '\t' * indent + '...'
		ctr += 1
		if isinstance(value, dict):
			pretty(value, indent+1)
		else:
			print '\t' * (indent+1) + str(value)

losses = [] 
for k in loss_dic:       
	losses.append(loss_dic[k])
figure(10);hist(losses)


for k in loss_dic:
	if loss_dic[k]>0.1:
		run_name,behavioral_mode,timestamp,run_code,seg_num,offset = k
		if behavioral_mode == 'Direct_Arena_Potential_Field':
			data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one)
			mi(data['left'][0]);pause(1)






def load_animate_hdf5(path,start_at_time=0):
	start_at(start_at_time)
	l,s=function_load_hdf5(path)
	img = False
	for h in range(len(s)):
		if type(img) != bool:
			img *= 0
			img += 128
			mi_or_cv2(img)
		pause(0.5)
		n = str(h)
		for i in range(len(s[n]['left'])):
			img = s[n]['left'][i]
			#print s[n][state][i]
			bar_color = [0,0,0]
			
			if s[n][state][i] == 1:
				bar_color = [0,0,255]
			elif s[n][state][i] == 6:
				bar_color = [255,0,0]
			elif s[n][state][i] == 5:
				bar_color = [255,255,0]
			elif s[n][state][i] == 7:
				bar_color = [255,0,255]
			else:
				bar_color = [0,0,0]
			if i < 2:
				smooth_steer = s[n][steer][i]
			else:
				smooth_steer = (s[n][steer][i] + 0.5*s[n][steer][i-1] + 0.25*s[n][steer][i-2])/1.75
			#print smooth_steer
			apply_rect_to_img(img,smooth_steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			apply_rect_to_img(img,s[n][motor][i],0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=False)
			mi_or_cv2(img)
A5 = load_animate_hdf5






def Timeseries_Segments_hdf5(d):
	D = {}
	D['path'] = d['path']
	True
	D['type'] = 'Timeseries_Segments_hdf5'
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Interface for loading timeseries segments from hdf5')
	def _load_hdf5(d):
		path = d['path']
		True
		F = h5py.File(path)
		Lb = F['labels']
		S = F['segments']
		return Lb,S
	def _load():
		labels,segments = _load_hdf5({'path':D['path']})
		True
		D['labels'] = {}
		for q in labels.keys():
			D['labels'][q] = labels[q]
		D['segments'] = {}
		for q in segments.keys():
			D['segments'][int(q)] = segments[q]
	def _get(d):
		label_name = None
		segment_num = None
		if 'label' in d:
			label_name = d['label']
		if 'segment' in d:
			segment_num = d['segment']
		assert(not(label_name == None and X == None))
		assert(not(label_name != None and X != None))
		True
		if label_name != None:
			return D['labels'][label_name]
		elif segment_num != None:
			return D['segments'][segment_num]
	D['get'] = _get

		
	_load()
	return D	


python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_7July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Orange_6July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Orange_8July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_8July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_6July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
