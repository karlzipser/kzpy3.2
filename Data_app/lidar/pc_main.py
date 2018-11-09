from kzpy3.vis3 import *
import kzpy3.Data_app.lidar.python_pointclouds6k as ppc

for a in Arguments:
	ppc.A[a] = Arguments[a]

ppc.A['ABORT'] = False

resize = ppc.resize_versions[0]
image_type = ppc.image_type_versions[0]

ppc.rospy.init_node('receive_pointclouds')
ppc.rospy.Subscriber('/os1_node/points', ppc.PointCloud2, ppc.points__callback)

threading.Thread(target=ppc.pointcloud_thread,args=[]).start()

mn,mx = -0.5,0.7 

show_durations = Timer(5)
Durations = {}
durations = ['log',]
for d in durations:
    Durations[d] = {}
    Durations[d]['timer'] = Timer()
    Durations[d]['list'] = []

while ppc.A['ABORT'] == False:
	dname = 'log'
    
	time.sleep(0.001)
	try:
		k = image_type+'_resized_'+resize
		if k in ppc.Images:
			img = ppc.Images[k]
			if image_type == 't':
				Durations[dname]['timer'].reset()  
				img = np.log10(img+0.001)
				img[img>mx] = mx
				img[img<mn] = mn
				if 'temporary':
					img[0,0] = mx; img[0,1] = mn
				Durations[dname]['list'].append(1000.0*Durations[dname]['timer'].time())
			mci(
				(z2o(img)*255).astype(np.uint8),
				scale=4.0,
				color_mode=cv2.COLOR_GRAY2BGR,
				title='from pc_main.py',
			)
			if show_durations.check():
				for d in durations:
					cg(d,':',dp(np.median(Durations[d]['list']),1),'ms')
					show_durations.reset()
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',emphasis=True)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

cr("pc_main.py done.")



"""
min_len = 3;e='z'
len_lst = len(lst)
if len_lst < min_len:
	print 'a'
	pass
elif len_lst > 1.2*min_len:
	print 'b'
	lst = lst[-min_len:]
else:
	print 'c'
	lst.pop(0)
print 'e'
lst.append(e)
"""