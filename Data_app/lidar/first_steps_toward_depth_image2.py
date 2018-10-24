
from kzpy3.vis3 import *

if 'O' not in locals():
	cs('loading O')
	O=h5r('/media/karlzipser/1_TB_Samsung_n1/h5py_/tegra-ubuntu_18Oct18_08h43m23s/original_timestamp_data.h5py' )
	#O=h5r('/media/karlzipser/1_TB_Samsung_n1/h5py_____/tegra-ubuntu_08Oct18_18h09m29s/original_timestamp_data.h5py')

p = O['points']['vals']

exception_timer = Timer(30)

us=[]

if True:


	left_ts = 0
	left_t = 0

	CA()

	for t in range(5000,15000):

		ts = O['points']['ts'][t]

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


		figure('lidar xy');clf();pts_plot(q[:,:2],sym=',');xylim(0,10,-5,5);spause()
		figure('lidar yz');clf();pts_plot(q[:,(0,2)],color='b',sym=',');xylim(0,10,-5,5);spause()
		mi(O['left_image']['vals'][left_t],'left')


		ctr1,ctr2=0,0

		Depths = {}
		zDepths = {}

		range_n180_180 = range(-180,180)
		range_0_360 = range(0,360)
		range_n360_360 = range(-360,360)
		range_n90_90 = range(-90,90)

		zrange = range(-15,16,2) 

		the_range = range_n180_180

		for b in zrange:
			Depths[b] = {}
			for a in the_range:
				Depths[b][a] = [0]

		for b in the_range:
			zDepths[b] = [0]

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
				#print bi
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
					file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					exc_type, exc_obj, exc_tb = sys.exc_info()
					cs(exc_type,file_name,exc_tb.tb_lineno,'exceptions are ',dp(100*ctr1/(1.0*ctr2)),"% of computations")
					exception_timer.reset()

		figure('m');clf();
		for b in zrange:
			print b
			m = []
			for ai in sorted(Depths[b]):
				if len(Depths[b][ai])>1:
					Depths[b][ai]=Depths[b][ai][1:]
				m.append(np.mean(Depths[b][ai]))
			#n[0:180] = m[180:360]
			#n[180:] = m[:180]
			plot(the_range,m);xylim(-180,180,0,4);spause()#xylim(90,270,0,8)#xylim(180-55,180+55,0,10,);
		#spause();raw_enter()
			#figure('n');clf();plot(m,'.');spause()#xylim(140,220,0,4);   xylim(180-55,180+55,0,10,);


		if False:
			zm = []
			for bi in sorted(zDepths):
				if len(zDepths[bi])>1:
					zDepths[bi]=zDepths[bi][1:]
				zm.append(np.min(zDepths[bi]))
			#zn[0:180] = zm[180:360]
			#zn[180:] = zm[:180]
			figure('zm');clf();plot(the_range,zm);spause()# xylim(90,270,0,8); #xylim(180-55,180+55,0,10,);


		"""
		for u in range(150,260):
			if zm[u] > 0.4:# and zn[u] < 1.1:
				us.append(u)
		figure('us');clf();hist(na(us)-180)
		"""




#EOF