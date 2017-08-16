
data_dic = {}

data_dic['GPS'] = {}
data_dic['acc'] = {}
data_dic['mo_sr'] = {}

path_to_data = '/Volumes/ZBDD_4TB/teg_data'
frame_folder = '_18Apr16_16h53m04s_caffe'
gps_acc_files = ['_18Apr16_17h15m44s.GPS_acc.txt','_18Apr16_16h49m55s.GPS_acc.txt','_18Apr16_16h48m46s.GPS_acc.txt']
mot_sr_files = ['_18Apr16_16h49m54s.motor_servo.txt','_18Apr16_17h15m43s.motor_servo.txt']

def gps_acc_data_to_dic(path_to_data,data_file,data_dic):
	r = txt_file_to_list_of_strings(opj(path_to_data,data_file))
	for b in r:
		if 'GPS' in b:
			try:
				exec('c='+b)

				data_dic['GPS'][c[-1]] = c[1:-1]
			except Exception,e:
				print e
		elif 'acc' in b:
			exec('c='+b)
			data_dic['acc'][c[-1]] = c[1:-1]

def motor_servo_data_to_dic(path_to_data,data_file,data_dic):
	r = txt_file_to_list_of_strings(opj(path_to_data,data_file))
	for b in r:
		try:
			exec('c='+b)
			data_dic['mo_sr'][c[-1]] = c[:-1]
		except Exception,e:
			print e

# First, load data into data_dic, which holds GPS, acc, motor and servo data.
# Each type of data is separately keyed on the timestamp. 
for d in gps_acc_files:
	gps_acc_data_to_dic(path_to_data,d,data_dic)

for d in mot_sr_files:
	motor_servo_data_to_dic(path_to_data,d,data_dic)

if False:
	# look at motor, servo and mode data
	m = []
	mst = sorted(data_dic['mo_sr'])
	for t in mst:
		m.append(data_dic['mo_sr'][t])
	m=np.array(m)
	plot(10*m[:,0]);plot(m[:,1]);plot(m[:,2]);

	# look at acc data
	acc_t = sorted(data_dic['acc'])
	xa = []
	ya = []
	za = []

	for t in acc_t:
		xyz = data_dic['acc'][t]
		xa.append(xyz[0])
		ya.append(xyz[1])
		za.append(xyz[2])

	plt.plot(acc_t,za,'b')
	plt.plot(smooth(np.array(za),window_len=50),'r')

	# look at GPS data
	lat_lon = []
	for c in data_dic['GPS']:
		d = data_dic['GPS'][c]
		if d[0] > 0:
			lat_lon.append([d[0],d[1]])
	lat_lon = np.array(lat_lon)
	plot(lat_lon[:,1],lat_lon[:,0],'o')


def estimate_frame_time(path_to_frame_folder,frame_folder,df=1./15.):
	frame_time_est = []
	_,frame_names = dir_as_dic_and_list(opj(path_to_frame_folder,frame_folder))
	ctime0 = os.path.getctime(opj(path_to_frame_folder,frame_folder,frame_names[0]))
	ctime0 += 3600 #!!!!!!! Note, the ctimes on the frames are not on daylight savings time !!!!!!
	ctr = 0.0
	for f in frame_names:
		frame_time_est.append(ctr*df+ctime0)
		ctr += 1.0
	return frame_time_est

frame_time_est = estimate_frame_time(path_to_data,frame_folder)

"""
# bin sensor data with reference to a frame series
ac = np.array(acc_t)
ft = np.array(frame_time_est)
ac -= ft[0] # time 0 of the frame series is the reference point
ac /= 1./15.
ac = np.round(ac)
ac_dic = {}
for i in range(len(ac)):
	a = ac[i]
	if a not in ac_dic:
		ac_dic[a] = []
	ac_dic[a].append(i)


z = []
for i in range(0,14000):
	try:
		z.append(za[int(ac_dic[i][0])])
	except Exception,e:
		print e
plot(z)
"""

def bin_sensor_data_wrt_frame_series(frame_ref_time,data_type,data_dic):
	"""
	Make a dictionary keyed on frame number that maps to data indicies
	"""
	ts_ = np.array(sorted(data_dic[data_type]))
	ts = ts_.copy()
	ts -= frame_ref_time
	ts /= 1.0/15.0
	ts = np.round(ts)
	ts_dic = {}
	for i in range(len(ts)):
		t = ts[i]
		if t not in ts_dic:
			ts_dic[t] = []
		ts_dic[t].append(i)
	return ts_dic,ts_


mo_sr_ts_dic,mo_sr_ts = bin_sensor_data_wrt_frame_series(frame_time_est[0],'mo_sr',data_dic)
acc_ts_dic,acc_ts = bin_sensor_data_wrt_frame_series(frame_time_est[0],'acc',data_dic)



s = []
for i in range(0,len(frame_time_est)):
	try:
		d = mo_sr_ts_dic[i]
		a = 0.0
		for i in range(len(d)):
			a += data_dic['mo_sr'][mo_sr_ts[d[i]]][1]
		s.append(a/(1.0*len(d)))

	except Exception,e:
		print e
plot((np.array(s)-49)/10)

for j in range(3):
	s = []
	for i in range(0,len(frame_time_est)):
		try:
			d = acc_ts_dic[i]
			a = 0.0
			for i in range(len(d)):
				a += data_dic['acc'][acc_ts[d[i]]][j]
			s.append(a/(1.0*len(d)))

		except Exception,e:
			print e
	plot(s)#plot(smooth(np.array(s)))



# http://www.scipy.org/Cookbook/SignalSmooth
def smooth(x,window_len=11,window='hanning'):
        if x.ndim != 1:
                raise ValueError, "smooth only accepts 1 dimension arrays."
        if x.size < window_len:
                raise ValueError, "Input vector needs to be bigger than window size."
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        s=np.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=np.ones(window_len,'d')
        else:  
                w=eval('np.'+window+'(window_len)')
        y=np.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]




ts = []
ds = []
l = txt_file_to_list_of_strings('/Volumes/ZBDD_4TB/teg_data_26April2016/ctimes__26Apr16_16h47m55s_caffe')
for m in l:
	ts.append(np.float(m.split(' ')[0]))
for i in range(len(ts)-1):
	ds.append(ts[i+1]-ts[i])
ds = np.array(ds)
print ds.mean()
hist(ds,100)

"""
def frame_ct(path_to_data,frame_folder):
	frame_to_ctime_dic = {}
	ctime_to_frame_dic = {}
	_,frame_names = dir_as_dic_and_list(opj(path_to_frame_folder,frame_folder))
	for f in frame_names:
		ctime = os.path.getctime(opj(path_to_frame_folder,frame_folder,f))
		#ctime += 3600 #!!!!!!! Note, the ctimes on the frames are not on daylight savings time !!!!!!
		frame_to_ctime_dic[opj(frame_folder,f)] = ctime
		ctime_to_frame_dic[ctime] = opj(frame_folder,f)
	return frame_to_ctime_dic,ctime_to_frame_dic
# frame_to_ctime_dic,ctime_to_frame_dic = frame_ct(path_to_frame_folder,frame_folder)

"""