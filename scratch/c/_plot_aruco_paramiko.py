#!/usr/bin/env python
from kzpy3.vis2 import *

#clf();plt_square();xysqlim(2.1);
img = zeros((210,210,3),np.uint8)
while True:
	if True:#try:
		l = txt_file_to_list_of_strings(opjD('Mr_Black.txt'))
		exec('pose = '+l[0])
		img[pose[0],pose[1],0]=255;
		mci(img,delay=5)
	else:#except:
		print 'oops'