


def zaccess(d,alst):
	print(zdic_to_str(d,alst))
	for a in alst:
		#print a,d
		if type(d) != dict:
			break
		d = d[sorted(d.keys())[a]]
	return d







def zlst_truncate(lst,show_ends=2):
	if show_ends == 0:
		return []
	if len(lst) > 2*show_ends:
		out_lst = lst[:show_ends] + ['...'] + lst[-show_ends:]
	else:
		out_lst = lst
	return out_lst

def zlst_to_str(lst,truncate=True,decimal_places=2,show_ends=2,depth=0,range_lst=[-2]):
	original_len = -1
	if truncate:
		original_len = len(lst)
		lst = zlst_truncate(lst,show_ends=show_ends)
	lst_str = d2n('\t'*(depth),"[")
	for i in range(len(lst)):
		e = lst[i]
		if type(e) == str:
			lst_str += e
		elif type(e) == int:
			lst_str += str(e)
		elif is_number(e):
			lst_str += str(dp(e,decimal_places))
		elif type(e) == list:
			lst_str += zlst_to_str(e,truncate=truncate,decimal_places=decimal_places,show_ends=show_ends)
		elif type(e) == dict:
			lst_str += zdic_to_str(d,range_lst,depth=depth+1)# zlst_to_str(e,truncate=truncate,decimal_places=decimal_places,show_ends=show_ends)
		else:
			lst_str += '???'
		if i < len(lst)-1:
			lst_str += ' '
	lst_str += ']'
	if original_len > 0:
		lst_str += d2n(' (len=',original_len,')')
	return lst_str





def zdic_to_str(d,range_lst,depth=0,dic_show_ends=4,dic_truncate=True):

	dic_str_lst = []

	sorted_keys = sorted(d.keys())
	
	this_range = range_lst[0]
	
	if type(this_range) == int:
		if this_range < 0:
			neg_two = False
			if this_range == -2:
				neg_two = True
			if dic_truncate:
				this_range = [0,min(dic_show_ends,len(sorted_keys))]
			else:
				this_range = [0,len(sorted_keys)]
			if neg_two:
				range_lst = range_lst + [-2]
		else:
			this_range = [this_range,this_range+1]

	if this_range[0] > 0:
		dic_str_lst.append(d2n('\t'*depth,'0) ...'))

	#truncated = False
	for i in range(this_range[0],this_range[1]):
		#if dic_truncate:
		#	if this_range[1] > 2*dic_show_ends:
		#		if i > this_range[0]+dic_show_ends and i < this_range[1]-dic_show_ends:
		#			if not truncated:
		#				dic_str_lst.append(d2n('\t'*depth,'...'))
		#				truncated = True
		#			continue
		if i >= len(sorted_keys):
			return
		key = sorted_keys[i]
		value = d[key]

		dic_str_lst.append(d2n('\t'*depth,i,') ',key,':'))

		if isinstance(value,dict):
			#if max_depth_lst[0] > depth:
			if len(range_lst) > 1:
				dic_str_lst.append( zdic_to_str(value,range_lst[1:],depth=depth+1,dic_show_ends=dic_show_ends,dic_truncate=dic_truncate) )
			else:
				dic_str_lst.append(d2n('\t'*(depth+1),'...'))
		else:
			if type(value) == list:
				dic_str_lst.append(zlst_to_str(value,depth=depth+1,range_lst=range_lst[1:]))
			elif type(value) == np.ndarray:
				dic_str_lst.append(zlst_to_str(list(value),depth=depth+1,range_lst=range_lst[1:]))
			elif type(value) == str:
				dic_str_lst.append(d2s('\t'*(depth+1),str(value)))
			else:
				dic_str_lst.append(d2s('\t'*(depth+1),str(value),type(value)))

	if this_range[1] < len(sorted_keys):
		dic_str_lst.append(d2n('\t'*depth,'... ',len(d)-1,')'))

	dic_str = ""
	for d in dic_str_lst:
		dic_str += d + "\n"

	return dic_str


def zprint_str_lst(str_lst):
	for s in str_lst:
		if type(s) == list:
			zprint_str_lst(s)
		else:
			print(s)

if False:
	a = {}
	a['a'] = 'A'
	a['b'] = {}
	a['b']['B1'] = {}
	a['b']['B1']['b1'] = 'a'
	a['b']['B2'] = [1,2,3,4,5]
	a['c'] = 'C'

	d = {}
	d['a'] = 'A'
	d['b'] = {}
	d['b']['B1'] = {}
	d['b']['B1']['b1'] = a
	d['b']['B2'] = [1,2,3,4,5]
	d['c'] = 'C'



	dic_str = zdic_to_str(d,[-2]);print dic_str


	figure('trajectories',figsize=(8,8))
	N = lo(opjD('N'))
	TOP = {}
	TOP['current_dic'] = N
	def zac(alst):
		return zaccess(TOP['current_dic'],alst)

	for i in range(len(zac([1]).keys())):
		x=zaccess(N,[1,i,1,1,2])
		y=zaccess(N,[1,i,1,1,4])
		clf();xylim(-5,5,-5,5)
		plot(x,y,'o');pause(2)

print_b = False;load_images=True
A=get_new_Data_dic()
meta_path='/Volumes/SSD_2TB/bair_car_data_new_28April2017/meta/direct_rewrite_test_28Apr17_17h50m34s_Mr_Black'
rgb_1to4_path='/Volumes/SSD_2TB/bair_car_data_new_28April2017/rgb_1to4/direct_rewrite_test_28Apr17_17h50m34s_Mr_Black'
multi_preprocess_pkl_files(A,meta_path,rgb_1to4_path,print_b,load_images,load_right_images=True)
import kzpy3.caf8.protos as protos
solver = protos.setup_solver(opjh('kzpy3/caf8/z2_color_aruco/solver.prototxt'))
solver.net.copy_from('/Users/karlzipser/caffe_models/z2_color_aruco_potential_May2017/z2_color_iter_6500000.caffemodel')
#solver.net.copy_from('/Users/karlzipser/caffe_models/z2_color/z2_color.caffemodel')
solver.net.blobs['metadata'].data[0,:,:,:] *= 0
solver.net.blobs['metadata'].data[0,3,:,:] = 1
for i in range(1000,len(A['left'])):
	ctr = 0
	for c in range(3):
		for camera in ['left','right']:
			for t in range(2):
				solver.net.blobs['ZED_data_pool2'].data[0,ctr,:,:] = A[camera][i][:,:,c]
				ctr += 1
	solver.net.forward()
	steer = 100*solver.net.blobs['ip2'].data[0,9]
	img = A['left'][i].copy()
	if np.mod(i,100) == 0:
		print i
	k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=1,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='plan')


"""

	Racing = 0
	Caf = 0
	Follow = 0
	Direct = 0
	Play = 0
	Furtive = 0
	if data['labels']['racing']:
		Racing = 1.0
	if data['states'][0] == 6:
		Caf = 1.0
	if data['labels']['follow']:
		Follow = 1.0
	if data['labels']['direct']:
		Direct = 1.0
	if data['labels']['play']:
		Play = 1.0
	if data['labels']['furtive']:
		Furtive = 1.0

	solver.net.blobs['metadata'].data[b,0,:,:] = Racing
	solver.net.blobs['metadata'].data[b,1,:,:] = Caf
	solver.net.blobs['metadata'].data[b,2,:,:] = Follow
	solver.net.blobs['metadata'].data[b,3,:,:] = Direct
	solver.net.blobs['metadata'].data[b,4,:,:] = Play
	solver.net.blobs['metadata'].data[b,5,:,:] = Furtive

"""
