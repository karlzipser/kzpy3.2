
from kzpy3.vis3 import *

if 'O' not in locals():
	cs('loading O')
	O=h5r('/media/karlzipser/1_TB_Samsung_n1/h5py_/tegra-ubuntu_18Oct18_08h43m23s/original_timestamp_data.h5py' )
	#O=h5r('/media/karlzipser/1_TB_Samsung_n1/h5py_____/tegra-ubuntu_08Oct18_18h09m29s/original_timestamp_data.h5py')

p = O['points']['vals']
exception_timer = Timer(30)
us=[]
if True:
	s = zeros((546,16))

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

		r = na(distances).reshape(1024,16)
		s[:(1024-918),:] = r[918:,:]
		s[106:,:] = r[:440,:]
		figure('lidar xy');clf();pts_plot(q[:,:2],sym=',');xylim(0,10,-5,5);spause()
		figure('lidar yz');clf();pts_plot(q[:,1:3],color='b',sym=',');xylim(0,10,-5,5);spause()
		mi(O['left_image']['vals'][left_t],'left')


		ctr1,ctr2=0,0
		Depths = {}
		zDepths = {}
		for a in range(-180,180):
			Depths[a] = [0]
		for b in range(-180,180):
			zDepths[b] = [0]

		n=zeros(360)
		zn=zeros(360)

		for i in range(1024*16):
			x = q[i,0]
			y = q[i,1]
			z = q[i,2]
			a = np.degrees(angle_between((1, 0), (x,y)) )
			b = np.degrees(angle_between((1, 0), (np.sqrt(x**2+y**2),z)))

			if y > 0:
				a*=-1
				b*=-1
			try:
				ctr2+=1

				ai = int(a)
				bi = int(b)
				if abs(bi) < 1:
					Depths[ai].append(distances[i])#np.sqrt(  q[i,0]**2 + q[i,1]**2 + q[i,2]**2))
				zDepths[bi].append(distances[i])#np.sqrt(  q[i,0]**2 + q[i,1]**2 + q[i,2]**2))

				
			except Exception as e:
				ctr1+=1
				if exception_timer.check():
					cs('exception',ctr1,ctr2,dp(100*ctr1/(1.0*ctr2)))
					exc_type, exc_obj, exc_tb = sys.exc_info()
					file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					CS_('Exception!',emphasis=True)
					CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
					exception_timer.reset()
		m = []
		for ai in Depths:
			if len(Depths[ai])>1:
				Depths[ai]=Depths[ai][1:]
			m.append(np.mean(Depths[ai]))
		n[0:180] = m[180:360]
		n[180:] = m[:180]
		figure('n');clf();plot(n,);xylim(90,270,0,8);spause()#xylim(180-55,180+55,0,10,);
		#figure('n');clf();plot(m,'.');spause()#xylim(140,220,0,4);   xylim(180-55,180+55,0,10,);


		zm = []
		for bi in zDepths:
			if len(zDepths[bi])>1:
				zDepths[bi]=zDepths[bi][1:]
			zm.append(np.mean(zDepths[bi]))
		zn[0:180] = zm[180:360]
		zn[180:] = zm[:180]
		figure('zn');clf();plot(zn);spause()# xylim(90,270,0,8); #xylim(180-55,180+55,0,10,);



		for u in range(150,260):
			if zn[u] > 0.4:# and zn[u] < 1.1:
				us.append(u)
		figure('us');clf();hist(na(us)-180)


			#440 918


if False:
	CA()
	Depths = {}
	q = p[5000,:,:].astype(np.float32)
	angles = []
	for i in range(1024*16):
		x = q[i,0]
		y = q[i,1]
		a = np.degrees(angle_between((1, 0), (x,y)) )
		ai = int(a)
		if ai not in Depths:
			Depths[ai] = []
		Depths[ai].append(np.sqrt(  q[i,0]**2 + q[i,1]**2 ))

	m = []
	for ai in Depths:
		m.append(np.median(Depths[ai]))
	#plot(angles,'k.')
	#hist(angles,bins = 500)