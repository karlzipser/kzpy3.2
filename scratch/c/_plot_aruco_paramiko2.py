#!/usr/bin/env python
from kzpy3.vis2 import *
clear_timer = Timer(1)

import kzpy3.Cars.robot_car_28Aug2017.nodes.runtime_parameters as rp

potential_image = imread(rp.potential_field_png)
potential_image = potential_image[:,:,0]
potential_image = (255*z2o(1.0*potential_image)).astype(np.int)
#mi(potential_image,'potential_image');spause()
from kzpy3.Grapher_app.Graph_Image_Module import *
wall_length = 4*107.0/100.0
half_wall_length = wall_length/2.0
hw = half_wall_length
x_min = -(6.03/2.0)
x_max = (6.03/2.0)
y_min = -(6.03/2.0)
y_max = 6.03/2.0
Gi = Graph_Image(xmin,x_min,
	xmax,x_max,
	ymin,y_min,
	ymax,y_max,
	xsize,shape(potential_image)[0],
	ysize,shape(potential_image)[1])
for i in range(3):
	Gi[img][:,:,i] = potential_image.copy()



Colors = {'Mr_Black':(255,0,0),'Mr_Blue':(0,0,255),'Mr_Lt_Blue':(50,200,255)}

done = False
while not done:
	try:
		something_happened = False

		for car in sggo(opjD('*.car.txt')):
			car_name = fname(car).split('.')[0]
			new_car = car.replace('car','')
			unix('cp '+car+' '+new_car)
			l = txt_file_to_list_of_strings(new_car)
			for ll in l:
				exec(ll)
			if len(pose) == 4:

				if clear_timer.check():

					clear_timer.reset()


				heading_floats = np.array(heading_floats)

				for xxyy in xy:

					Gi[img][int(xxyy[0]),int(xxyy[1]),:] = [0,150,10]

				car_color = Colors[car_name]
				Gi[ptsplot](x,[pose[0]],y,[pose[1]],color,car_color)
				Gi[ptsplot](x,[pose[0]+pose[2]],y,[pose[1]+pose[3]],color,(0,255,0))
				something_happened = True

		if something_happened:
			k = mci(Gi[img],delay=5,scale=30)
			if k == ord('q'):
				done = True
				break
		if True:#k == ord('r'):
				for i in range(3):
					Gi[img][:,:,i] = potential_image.copy()
	
	except (KeyboardInterrupt, SystemExit):
		raise
	except Exception as e:
		print("********** Exception ***********************")
		print(e.message, e.args)
	