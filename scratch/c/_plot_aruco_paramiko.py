#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)
#clf();plt_square();xysqlim(2.1);

from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
Gi = Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,100, ysize,100)



while True:
	try:
		l = txt_file_to_list_of_strings(opjD('Mr_Black.txt'))
		exec('pose = '+l[0])
		if len(pose) == 4:
			if clear_timer.check():
				img *= 0
				clear_timer.reset()
				x1,y1 = Gi[ptsplot](x,pose[0],y,pose[1],color,(255,0,0))
		k = mci(Gi[img],delay=5)
		if k == ord('q'):
			break
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		raise
		print(d2s('oops',time.time()))
