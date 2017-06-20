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

