
from kzpy3.utils2 import *

def identify_bagfiles(volume_name=''):
	Bagfiles = {}
	for dirpath, dirnames, filenames in os.walk(opjm(volume_name)):
	    for filename in [f for f in filenames if f.endswith(".bag")]:
	    	if not (filename in Bagfiles):
	    		Bagfiles[filename] = []
	    	new_dirpath = dirpath.relpace(opjm(volume_name),'')
	    	Bagfiles[filename].append(opj(new_dirpath,filename))
	    	print Bagfiles[filename][-1]
	return Bagfiles

B = identify_bagfiles(volume_name='model_car_data_A1')