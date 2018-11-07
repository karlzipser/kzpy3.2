#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

calls = 0
calls_prev = 0
timer = Timer(7)
P = []
ary = zeros(64*1024)
if True:
    def points__callback(msg):
        global P
        global calls
        calls += 1
        #p = list(pc2.read_points(msg,skip_nans=False,field_names=['t','intensity','reflectivity']))#,'intensity']))
	
	ctr = 0
	for point in pc2.read_points(msg,skip_nans=False,field_names=['t','intensity','reflectivity']):
		ary[ctr]=point[0]	
		ary[ctr]=point[1]
		#ary[ctr]=point[2]
		ctr+=1
        #p = na(p)
        #p[np.isnan(p)] = 0
        #advance(P,p,2)


    rospy.init_node('receive_pointclouds')

    rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

    waiting = Timer(1)

    while calls < 1:
        waiting.message('waiting for data')
        time.sleep(0.01)

    freq_timer = Timer(1);



    Y = {}
    mx = 6290
    for d in range(0,mx+30):
        v = int(1024 * d / (1.0*mx))
        if v > 1023:
            v = 1023
        Y[d] = v

    j = 0
    for i in range(sorted(Y.keys())[-1]):
        if i in Y:
            j = Y[i]
        Y[i] = j

    Y[np.nan] = 0



    while not timer.check():

        #waiting.message(d2s('Processing ROSbag data...',time_str()))

        try:
	    #freq_timer.freq()
            calls_ = calls
	    #print calls
            if calls_ > calls_prev:
		freq_timer.freq()
		t0=time.time()
		#pd2s("calls step",calls_-calls_prev)
	    	freq_timer.freq()
		# 8.7 Hz	
                #a = na(P[-1])
		# 5.3 Hz
			
                #print type(a),shape(a),shape(P[-1][0]),shape(P[-1][1])
		
                #b = a[:65536,1].reshape(1024,64)
		b = ary.reshape(1024,64)
		# 5 Hz
		# from kzpy3.Data_app.lidar.python_pointclouds6c_ import *
		plot(b);xlim(0,1023);spause();raw_enter()
		
		c=b[:,1:64:4] 
		#print c.max(),c.min()
		y = (c[:,8]).astype(int)
		#y = (c[:,8]*1000).astype(int)
		indicies=[]
		if False:#for v in y:
			#print v
			if v in Y:
				#print Y[v]
				indicies.append(Y[v])
			else:
				pd2s("v not in Y",v,type(v))
				indicies.append(0)
		indicies = [Y[v] for v in y]
		d = 0*c 	
		d[indicies,:] = c
                for i in range(1,len(d)):
                        if d[i,0] == 0:
                                d[i,:] = d[i-1,:]

		plot(d);xlim(0,1023);spause();raw_enter()
		#mi(d.transpose(1,0));spause();raw_enter()
		print time.time()-t0	
            calls_prev = calls_
        except:
            cs('exception',calls)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)






#EOF
