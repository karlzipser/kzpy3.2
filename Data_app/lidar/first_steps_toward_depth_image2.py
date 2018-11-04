
from kzpy3.vis3 import *
#the_run,the_start_index = 'tegra-ubuntu_18Oct18_08h43m23s',830
#the_run,the_start_index = 'tegra-ubuntu_18Oct18_08h14m24s_b',630
#the_run,the_start_index = 'tegra-ubuntu_16Oct18_11h24m21s',1000
#the_run,the_start_index = 'tegra-ubuntu_16Oct18_17h02m43s',1000
#the_run,the_start_index = 'tegra-ubuntu_16Oct18_17h42m25s',700
#the_run,the_start_index = 'tegra-ubuntu_17Oct18_12h11m22s',1000
#the_run,the_start_index = 'tegra-ubuntu_17Oct18_12h46m32s',1000
# #nothing: the_run,the_start_index = 'tegra-ubuntu_18Oct18_08h14m24s_a',700
# another one in the same folder is also nothing.

#run_folders = sggo('/media/karlzipser/1_TB_NTFS_1/*')
run_folders = sggo('/media/karlzipser/1_TB_Samsung_n1/*')


temp = sggo(opjD('Depth_images/*'))
runs_in_progress_or_done = []
for t in temp:
	runs_in_progress_or_done.append(fname(t).split('.')[0])
run_folder = False
for f in run_folders:
	for r in sggo(f,'*'):
		if 'Mr_Black' not in r:
			if fname(r) not in runs_in_progress_or_done:
				run_folder = r
		if run_folder:
			break
	if run_folder:
		break

run_folder = '/media/karlzipser/1_TB_Samsung_n1/tu_25to26Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_25Oct18_16h17m55s'





def process_and_save_Depth_images(run_folder):

	the_run = fname(run_folder)

	os.system(d2s("touch",opjD('Depth_images',the_run)))

	if 'O' not in locals():
		cs('loading O')
		O=h5r(opj(run_folder,'original_timestamp_data.h5py' ))
		#O=h5r('/media/karlzipser/1_TB_Samsung_n1/h5py_____/tegra-ubuntu_08Oct18_18h09m29s/original_timestamp_data.h5py')

	p = O['points']['vals']

	exception_timer = Timer(30)
	print_timer = Timer(10)
	us=[]

	timer = Timer()

	Depth_images = {}
	Depth_images['run'] = the_run
	Depth_images['ts'] = []
	Depth_images['index'] = []
	Depth_images['real'] = []
	Depth_images['display'] = []



	left_ts = 0
	left_t = 0

	CA()

	range_n180_180 = range(-180,180)
	range_0_360 = range(0,360)
	range_n360_360 = range(-360,360)
	range_n90_90 = range(-90,90)
	range_n55_55 = range(-55,55)
	range_n60_60 = range(-60,60)


	zrange = range(-15,16,2)
	zranger = range(15,-16,-2)
	#zranger.remove(-13) ### This z-level seems to give no signal

	the_range = range_n60_60

	depth_img = zeros((32,len(the_range)))
	depth_img_prev = depth_img.copy()

	ctr1,ctr2=0,0
	the_encoder_index = 0
	while O['encoder']['vals'][the_encoder_index] < 0.75:
		the_encoder_ts = O['encoder']['ts'][the_encoder_index]
		the_encoder_index += 1
	
	spd2s(the_encoder_ts)

	for t in range(len(p)):

		ts = O['points']['ts'][t]
		print t,ts,the_encoder_ts
		if ts < the_encoder_ts:
			continue

		print_timer.message(d2s("ts =",ts,"t =",t,"(",len(p),")"))
		left_ts = O['left_image']['ts'][left_t]
		while left_ts < ts:
			left_t += 1
			left_ts = O['left_image']['ts'][left_t]

		q = p[t,:,:].astype(np.float32)

		"""
		distances = []

		for i in range(1024*16):
			x = q[i,0]
			y = q[i,1]
			z = q[i,2]
			dist = np.sqrt( x**2 + y**2 + z**2 )
			distances.append(dist)
		"""

		#figure('lidar xy');clf();pts_plot(q[:,:2],sym=',');xylim(0,10,-5,5);spause()
		#figure('lidar yz');clf();pts_plot(q[:,(0,2)],color='b',sym=',');xylim(0,10,-5,5);spause()
		mi(O['left_image']['vals'][left_t],d2n(the_run,': left'))


		Depths = {}
		#zDepths = {}





		for b in zrange:
			Depths[b] = {}
			for a in the_range:
				Depths[b][a] = [0]

		#for b in the_range:
		#	zDepths[b] = [0]


		#n=zeros(360)
		#zn=zeros(360)

		for i in range(1024*16):

			x = q[i,0]
			y = q[i,1]
			z = q[i,2]

			a = np.degrees(angle_between((1,0), (x,y)) )

			if np.abs(a) <= 1.1*the_range[-1]:

				b = np.degrees(angle_between((1,0), (np.sqrt(x**2+y**2),z)))

				if y > 0:
					a*=-1
					#b*=-1

				if z < 0:
					b *= -1
				
				try:
					ctr2+=1
					ai = int(a)
					bi = b +0.5
					if bi < -15:
						bi = -15
					elif bi < -13:
						bi = -13
					elif bi < -11:
						bi = -11
					elif bi < -9:
						bi = -9
					elif bi < -7:
						bi = -7
					elif bi < -5:
						bi = -5
					elif bi < -3:
						bi = -3
					elif bi < -1:
						bi = -1
					elif bi < 1:
						bi = 1
					elif bi < 3:
						bi = 3
					elif bi < 5:
						bi = 5
					elif bi < 7:
						bi = 7
					elif bi < 9:
						bi = 9
					elif bi < 11:
						bi = 11
					elif bi < 13:
						bi = 13
					else:
						bi = 15

					dist = np.sqrt( x**2 + y**2 + z**2 )
					#if abs(bi) < 1:
					Depths[bi][ai].append(dist)#distances[i])#np.sqrt(  q[i,0]**2 + q[i,1]**2 + q[i,2]**2))
					#zDepths[bi].append(distances[i])#np.sqrt(  q[i,0]**2 + q[i,1]**2 + q[i,2]**2))

				
				except Exception as e:
					ctr1+=1
					if exception_timer.check():
						exc_type, exc_obj, exc_tb = sys.exc_info()
						file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
						cs(exc_type,file_name,exc_tb.tb_lineno,'exceptions are ',dp(100*ctr1/(1.0*ctr2)),"% of computations")
						exception_timer.reset()

		depth_img *= 0

		#figure('m');clf();
		ctr_10 = 0
		for b in zranger:
			#print b
			m = []
			ctr_11 = 0
			for ai in sorted(Depths[b]):
				if len(Depths[b][ai])>1:
					#Depths[b][ai]=Depths[b][ai][1:]
					#m.append(np.mean(Depths[b][ai]))
					m.append(np.mean(Depths[b][ai][1:]))
				else:
					m.append(0)#depth_img_prev[ctr_10,ctr_11])
					#pd2s('here',timer.time())
				ctr_11 += 1
			#n[0:180] = m[180:360]
			#n[180:] = m[:180]
			#plot(the_range,m);xylim(-180,180,0,4);spause()#xylim(90,270,0,8)#xylim(180-55,180+55,0,10,);
			for dd in range(2):
				depth_img[ctr_10,:] = m
				ctr_10 += 1
		#spause();raw_enter()
			#figure('n');clf();plot(m,'.');spause()#xylim(140,220,0,4);   xylim(180-55,180+55,0,10,);
		Depth_images['ts'].append(ts)
		Depth_images['index'].append(t)
		Depth_images['real'].append(depth_img.copy())
		#depth_img_rev = depth_img.copy()
		
		depth_img_prev = depth_img.copy()
		#depth_img *= 0
		#depth_img_rev=np.log10(depth_img_rev)
		#depth_img_rev[depth_img_rev>3.]=3.
		#depth_img[depth_img<0.6]=0.6
		#depth_img_rev =  1-z2o(depth_img_rev)#z2o(1/(depth_img))
		#depth_img_rev =  -depth_img_rev
		#Depth_images['display'].append(depth_img_rev.copy())
		figure(d2n(the_run,': depth_img'),figsize=(2,1))
		mi(depth_img,d2n(the_run,': depth_img'));
		plt.title('index')
		spause()

	try:
		os.system(d2s("rm",opjD('Depth_images',the_run)))
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',emphasis=True)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
		
	save_Depth_images(Depth_images,the_run)





def show_depth_imgs(Depth_images,start=0,stop=-1):
	#start=-500;stop=-1
	if type(Depth_images['run']) == str:
		the_run = Depth_images['run']
	else:
		the_run = Depth_images['run'][0] # because of hdf5 strings

	for img,index in zip(Depth_images['real'][start:stop],Depth_images['index'][start:stop]):
		figure(d2s(the_run,'show_depth_imgs'),figsize=(2,1))
		mi(img,d2s(the_run,'show_depth_imgs'));
		plt.title(index)
		spause()

#show_depth_imgs(F)




def save_Depth_images(Depth_images,the_run,path=opjD('Depth_images')):
	D = Depth_images
	file_path = opj(path,d2p(the_run,'Depth_image','h5py'))
	F = h5w(file_path)
	pd2s('saving',the_run,'Depth_images')

	for topic_ in Depth_images.keys():
		pd2s('\t',topic_,len(D[topic_]))
		cs( type(D[topic_]),shape(D[topic_]))
		if type(D[topic_]) == str:
			s = F.create_dataset(topic_,(1,),dtype=h5py.special_dtype(vlen=str))
			s[:] = the_run
		else:
			F.create_dataset(topic_,data=D[topic_])		
	F.close()

#save_Depth_images(Depth_images)

############################
#
process_and_save_Depth_images(run_folder)
#
#	python kzpy3/Data_app/lidar/first_steps_toward_depth_image2.py 
#
############################









if False:
	depth_image_files = sggo(opjD('Depth_images','*.h5py'))
	
	#depth_image_file = '/home/karlzipser/Desktop/Depth_images/tegra-ubuntu_26Oct18_08h37m07s.Depth_image.h5py'
	for depth_image_file in depth_image_files:

		error_file = depth_image_file+'.error'
		touched_file = depth_image_file+'.work_in_progress'
		if len(sggo(touched_file)) > 0:
			continue
		if len(sggo(error_file)) > 0:
			continue
			
		os.system(d2s('touch',touched_file))
		log_min,log_max = -0.25,1.5

		try:
			D=h5rw(depth_image_file)
			r=D['real'][:]
			pa = Progress_animator(len(r),message='r')

			display = False
			r[:,28,:] = r[:,27,:]
			r[:,29,:] = r[:,30,:]

			g = zeros((33,120))
			z = zeros((32,120))
			e = r[0,:,:]

			processed_depth_images = []

			display_timer = Timer(2)

			clear_screen()
			cs("Processing",depth_image_file)
			for i in rlen(r):

				pa['update'](i)

				if i > 0:
					a=r[i,:,:]
					b = a==0.0
					c = b.astype(int)
					d = (1-c)*a + c*e
					e = d.copy()
					f = np.log10(d+.001)
					h = (f>log_max).astype(int)
					k = (1-h)*f + h*(z+log_max)
					h = (f<log_min).astype(int)
					k = (1-h)*k + h*(z+log_min)
					if i == 1:
						processed_depth_images.append(k)
						# since first image has no previous, make first image equal second
					processed_depth_images.append(k)
					if display_timer.check():
						g[:32,:] = k
						g[32,0] = 1.5
						g[32,1:] = -0.25
						mi(1-g,'log10 depth image')
						if False:
							figure('hist');clf()
							hist(d.flatten(),bins=100);xylim(0,100,0,200)
							figure('log10 hist');clf()
							hist(k.flatten(),bins=100);xylim(-2,2,0,200)
						display_timer.reset()
				spause()
			assert len(processed_depth_images) == len(D['index'][:])
			D.create_dataset('log',data=na(processed_depth_images))
			D.close()
			os.system('rm '+touched_file)
			os.system(d2s('mv',depth_image_file,depth_image_file.replace('image.','images.')))
			
		except Exception as e:
			os.system('rm '+touched_file)
			os.system('touch '+error_file)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			CS_('Exception!',emphasis=True)
			CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)











if False:

	depth_image_files = sggo(opjD('Depth_images','*.Depth_images.h5py'))
	
	for depth_image_file in depth_image_files:

		error_file = depth_image_file+'.error'
		touched_file = depth_image_file+'.work_in_progress'
		if len(sggo(touched_file)) > 0:
			continue
		if len(sggo(error_file)) > 0:
			continue
			
		os.system(d2s('touch',touched_file))
		log_min,log_max = -0.25,1.5

		try:
			D=h5rw(depth_image_file)
			r=D['log'][:]
			#raw_enter()
			pa = Progress_animator(len(r),message='r')

			processed_depth_images = []

			display_timer = Timer(2)

			#clear_screen()
			cs("\n\nProcessing",depth_image_file,"for log flip.")
			for i in rlen(r):

				pa['update'](i)

				processed_depth_images.append(cv2.flip(r[i,:,:],1))
				if display_timer.check():
					mi(r[i,:,:],'log depth image')
					mi(processed_depth_images[-1],'log flip depth image')
					display_timer.reset()
				spause()
			assert len(processed_depth_images) == len(D['index'][:])
			D.create_dataset('log_flip',data=na(processed_depth_images))
			D.close()
			os.system('rm '+touched_file)
			os.system(d2s('mv',depth_image_file,depth_image_file.replace('_images.','_images.with_flip.')))
			
		except Exception as e:
			D.close()
			os.system('rm '+touched_file)
			os.system('touch '+error_file)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			CS_('Exception!',emphasis=True)
			CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
			break





if False:

	import kzpy3.Data_app.classify_data as classify_data
	P = {}
	P['experiments_folders'] = []
	classify_data.find_locations(opjm("1_TB_Samsung_n1"),P['experiments_folders'])
	P['experiments_folders'] = list(set(P['experiments_folders']))

	P['run_name_to_run_path'] = {}

	for experiments_folder in P['experiments_folders']:
		if fname(experiments_folder)[0] == '_':
			continue
		print experiments_folder
		locations = sggo(experiments_folder,'*')
		for location in locations:
			if fname(location)[0] == '_':
				spd2s('ignoring',location)
				continue
			print location
			b_modes = sggo(location,'*')
			print b_modes
			for e in b_modes:
				if fname(e)[0] == '_':
					continue
				if fname(e) == 'racing':
					continue
				spd2s(fname(e))
				for r in sggo(e,'h5py','*'):
					run_name = fname(r)
					P['run_name_to_run_path'][run_name] = r
					cg(sggo(r,'left_timestamp_metadata_right_ts.h5py'))


	depth_image_files = sggo(opjD('Depth_images','*.Depth_images.with_flip.with_flip.h5py'))
	

	for depth_image_file in depth_image_files:

		run_name = fname(depth_image_file.split('.')[0])
		assert run_name in P['run_name_to_run_path']
		cg(run_name)

		error_file = depth_image_file+'.error'
		touched_file = depth_image_file+'.work_in_progress'
		if len(sggo(touched_file)) > 0:
			continue
		if len(sggo(error_file)) > 0:
			continue
			
		os.system(d2s('touch',touched_file))


		try:
			D = h5rw(depth_image_file)
			index = D['index'][:]
			lidar_ts = D['ts'][:]
			L = h5r(opj(P['run_name_to_run_path'][run_name],'left_timestamp_metadata_right_ts.h5py'))
			left_camera_ts = L['ts'][:]
			L.close()

			

			display_timer = Timer(2)

			cs("\n\nProcessing",depth_image_file,"for left timestamps.")

			lidar_index = 0

			D_left_to_lidar_index = 0 * left_camera_ts

			len_left_ts = len(left_camera_ts)

			pa = Progress_animator(len_left_ts,message='r')

			finished = False

			for i in range(len_left_ts):
				if finished:
					break


				pa['update'](i)

				left_ts = left_camera_ts[i]

				while lidar_ts[lidar_index] < left_ts:

					if lidar_index >= len(lidar_ts)-1:
						finished = True
					if finished:
						break

					lidar_index += 1
					pa = Progress_animator(len(index),message=d2s(left_ts))

				cg(dp(lidar_ts[lidar_index]-left_ts,3),lidar_index,i)

				D_left_to_lidar_index[i] = lidar_index


			D.create_dataset('left_to_lidar_index',data=D_left_to_lidar_index)
			D.close()
			os.system('rm '+touched_file)
			os.system(d2s('mv',depth_image_file,depth_image_file.replace('_images.with_flip.with_flip','_images.with_flip.with_left_ts')))
			
		except Exception as e:
			D.close()
			os.system('rm '+touched_file)
			os.system('touch '+error_file)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			CS_('Exception!',emphasis=True)
			CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
	







"""
code_to_code_str(opjk("Data_app/lidar/first_steps_toward_depth_image2.py"))
"""
#EOF
