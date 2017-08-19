#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)
#clf();plt_square();xysqlim(2.1);
import kzpy3.Cars.robot_car_6Aug2017_temp.nodes.runtime_parameters as rp

#  b=cv2.blur(a,(40,40)) 

from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
img_ = cv2.blur(lo(opjD('Potential_graph_img')),(rp.potential_graph_blur,rp.potential_graph_blur))
Gi = Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,400, ysize,400)
for i in range(3):
	Gi[img][:,:,i] = imresize(img_,(400,400))

done = False
while not done:
	try:
		for car in ['Mr_Black.car.txt','Mr_New.car.txt']:
			l = txt_file_to_list_of_strings(opjD(car))
			for ll in l:
				exec(ll)
			if len(pose) == 4:
				#print pose
				if clear_timer.check():
					#img *= 0
					clear_timer.reset()
				Gi[ptsplot](x,[pose[0]],y,[pose[1]],color,(255,0,0))
				Gi[ptsplot](x,[pose[0]+pose[2]],y,[pose[1]+pose[3]],color,(0,255,0))
				for xxyy in xy:
					Gi[img][xxyy[0],[xxyy[1]],2] = 255 
				heading_floats = np.array(heading_floats)
				Gi[ptsplot]( x,heading_floats[:,0], y,heading_floats[:,1], color,(255,255,255), NO_REVERSE,False)
				k = mci(Gi[img],delay=5,scale=2)
			if k == ord('q'):
				done = True
				break
			if k == ord('r'):
				for i in range(3):
					Gi[img][:,:,i] = imresize(img_,(400,400))
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		raise
		print(d2s('oops',time.time()))
