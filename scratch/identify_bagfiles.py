
from kzpy3.utils2 import *

def identify_bagfiles(volume=''):
	Bags = {}
	for dirpath, dirnames, filenames in os.walk(opjm(volume)):
	    for filename in [f for f in filenames if f.endswith(".bag")]:
	    	if not (filename in Bags):
	    		Bags[filename] = []
	    	new_dirpath = dirpath.replace(opjm(volume),'')
	    	Bags[filename].append(opj(new_dirpath,filename))
	    	print Bags[filename][-1]
	Bagfiles = {'bags':Bags,'volume':volume}
	return Bagfiles

B = identify_bagfiles(volume='model_car_data_A1')