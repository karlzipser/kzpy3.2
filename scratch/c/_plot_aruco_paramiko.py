#!/usr/bin/env python
from kzpy3.vis2 import *

clf();plt_square();xysqlim(2.1);

while True:
	try:
		l = txt_file_to_list_of_strings(opjD('Mr_Black.txt'))
		exec('pose = '+l[0])
		plot(pose[0],pose[1],'ro');spause()
	except:
		print 'oops'