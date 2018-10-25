
from kzpy3.vis3 import *
the_run = 'tegra-ubuntu_18Oct18_08h43m23s'
if 'O' not in locals():
	cs('loading O')
	O=h5r('/media/karlzipser/1_TB_NTFS_1/h5py_/'+the_run+'/original_timestamp_data.h5py' )
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

if True:


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
	zranger.remove(-13) ### This z-level seems to give no signal

	the_range = range_n60_60

	depth_img = zeros((32,len(the_range)))
	depth_img_prev = depth_img.copy()

	ctr1,ctr2=0,0

	for t in range(830,len(p),1):#830

		ts = O['points']['ts'][t]

		print_timer.message(d2s("ts =",ts,"t =",t,"(",len(p),")"))
		left_ts = O['left_image']['ts'][left_t]
		while left_ts < ts:
			left_t += 1
			left_ts = O['left_image']['ts'][left_t]

		q = p[t,:,:].astype(np.float32)

		distances = []

		for i in range(1024*16):
			x = q[i,0]
			y = q[i,1]
			z = q[i,2]
			dist = np.sqrt( x**2 + y**2 + z**2 )
			distances.append(dist)


		#figure('lidar xy');clf();pts_plot(q[:,:2],sym=',');xylim(0,10,-5,5);spause()
		#figure('lidar yz');clf();pts_plot(q[:,(0,2)],color='b',sym=',');xylim(0,10,-5,5);spause()
		mi(O['left_image']['vals'][left_t],'left')


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

				#if abs(bi) < 1:
				Depths[bi][ai].append(distances[i])#np.sqrt(  q[i,0]**2 + q[i,1]**2 + q[i,2]**2))
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
					m.append(depth_img_prev[ctr_10,ctr_11])
					pd2s('here',timer.time())
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
		mi(depth_img,'depth_img');spause()




#EOF