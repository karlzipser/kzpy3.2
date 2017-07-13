from kzpy3.teg7.data.preprocess_bag_data import *

run_paths = sgg(opjD('bair_car_data','meta','*'))

for r in run_paths:
	if 'lost' not in r:

		Bag_Folder_filename = gg(opj(r,'Bag_Folder*'))[0]
		B = load_obj(Bag_Folder_filename)
		ts = B['data']['raw_timestamps']
		dts = B['data']['raw_timestamp_deltas']
		dts_hist = []

		for i in range(len(dts)):
			dt = dts[i]
			if dt > 0.3:
				dt = 0.3
			dts_hist.append(dt)

		figure(1)
		clf()
		plot(ts,dts)
		plt.ylim(0,1.3)
		plt.title(fname(r))
		#if 'state_one_steps' in B['data']:
		#	plot(ts,B['data']['state_one_steps']/2000.,'o')
		plot(ts,B['data']['state']/10.,'o')
		plot(B['data']['good_start_timestamps'],0.15+0.0*array(B['data']['good_start_timestamps']),'x')
		plot(ts,dts)

		figure(2)
		clf()
		plot(ts,B['data']['steer'],'r')
		plot(ts,B['data']['motor'],'b')
		plot(B['data']['good_start_timestamps'],49+0.0*array(B['data']['good_start_timestamps']),'gx')
		plt.ylim(-10,110)

		figure(5)
		clf()
		hist(dts_hist)
		plt.xlim(0,0.3)
		plt.title(fname(r))

		pause(0.1)


"""
% in each state
% good
state 1 only version (10 state one steps)
state 1 only version (30 state one steps)
state 6 only version (30 state one steps) w/smoothing
state 6 only version (60 state one steps) w/smoothing
"""

"""
import matplotlib
f = figure(1)
a = f.add_subplot(111)
r=matplotlib.patches.Rectangle((0,0),100,200,color='gray')
a.add_patch(r)
plt.xlim(0,300)
plt.ylim(0,300)
"""

pass

