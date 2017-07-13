from kzpy3.utils import *

okay_for_intial_training = sgg(opj('/home/karlzipser/Desktop/bair_car_data/previews/okay_for_initial_training','*'))

meta = sgg(opj('/home/karlzipser/Desktop/bair_car_data/meta','*'))

to_transfer = []

for i in range(len(meta)):
	meta[i] = fname(meta[i])

for o in okay_for_intial_training:
	if fname(o) not in meta:
		c = 'yellow'
		unix('mv '+'/home/karlzipser/Desktop/bair_car_data/temp_meta_location/unclassified/'+fname(o)+' /home/karlzipser/Desktop/bair_car_data/temp_meta_location/good_for_intial_training')
	else:
		c = 'blue'
	cprint(fname(o),c)
