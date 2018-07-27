
from kzpy3.utils2 import *

def identify_bagfiles(volume=''):
	Bags = {}
	for dirpath, dirnames, filenames in os.walk(opjm(volume)):
	    for filename in [f for f in filenames if f.endswith(".bag")]:
	    	if not (filename in Bags):
	    		Bags[filename] = []
	    	new_dirpath = dirpath.replace(opjm(volume),'')
	    	Bags[filename].append(opj(new_dirpath,filename))
	    	#print Bags[filename][-1]
	Bagfiles = {'bags':Bags,'volume':volume}
	return Bagfiles

B1 = identify_bagfiles(volume='model_car_data_A1')['bags']
B2 = identify_bagfiles(volume='model_car_data_A2')['bags']

Bags = {}
ctr = 0
for B in [B1,B2]:
	for k in B.keys():
		if not (k in Bags):
			Bags[k] = 0
		Bags[k] += 1
		ctr += 1

for k in Bags.keys():
	if Bags[k] < 3:
		pd2s(k,'!!!')

print ctr

