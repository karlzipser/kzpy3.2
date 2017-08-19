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
#img_ = z2o(cv2.blur(lo(opjD('Potential_graph_img')),(rp.potential_graph_blur,rp.potential_graph_blur)))
img_ = ((np.array(lo(opjD('Potential_graph_img'))))*255.0).astype(np.int)

#mi(img_);spause()
Gi = Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,25, ysize,25)
for i in range(3):
	Gi[img][:,:,i] = img_.copy()#imresize(img_,(400,400))

done = False
while not done:
	try:
		for car in ['Mr_Black.car.txt','Mr_New.car.txt']:
			l = txt_file_to_list_of_strings(opjD(car))
			for ll in l:
				exec(ll)
			if len(pose) == 4:

				if clear_timer.check():

					clear_timer.reset()


				heading_floats = np.array(heading_floats)
				#Gi[ptsplot]( x,heading_floats[:,0], y,heading_floats[:,1], color,(255,255,255), NO_REVERSE,False)

				for xxyy in xy:
					#print xxyy
					Gi[img][xxyy[0],xxyy[1],:] = [0,0,255]
					#print Gi[img][xxyy[0],xxyy[1],:]
				
				Gi[ptsplot](x,[pose[0]],y,[pose[1]],color,(255,0,0))
				Gi[ptsplot](x,[pose[0]+pose[2]],y,[pose[1]+pose[3]],color,(0,255,0))

				k = mci(Gi[img],delay=5,scale=10)
			if k == ord('q'):
				done = True
				break
			if k == ord('r'):
				for i in range(3):
					Gi[img][:,:,i] = img_.copy()#imresize(img_,(400,400))
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		#raise
		print(d2s('oops',time.time()))
