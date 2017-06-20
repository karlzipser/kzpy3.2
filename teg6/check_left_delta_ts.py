from kzpy3.teg4.data.preprocess.preprocess_bag_data import *

run_paths = sorted(gg('/media/karlzipser/rosbags/new/*'))

for r in run_paths:
	if 'lost' not in r:
		#preprocess_bag_data(r)
		L = load_obj(opj(r,'.preprocessed2/left_image_bound_to_data.pkl'))

		ts = sorted(L.keys())

		dts = []

		for i in range(1,len(ts)):
			dt = ts[i]-ts[i-1]
			if dt > 1.2:
				dt = 1.2
			dts.append(dt)
		figure(1)
		clf()
		plot(ts[1:],dts)
		figure(5);clf();hist(dts)
		pause(0.01)