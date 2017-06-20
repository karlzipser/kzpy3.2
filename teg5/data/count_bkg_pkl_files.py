path0 = '/home/karlzipser/Desktop/bair_car_data/rgb_1to4'

folders = sgg(opj(path0,'*'))
bags = 0
for f in folders:
	bags += len(sgg(opj(f,'*.bag.pkl')))
bags