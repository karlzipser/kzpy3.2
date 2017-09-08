from kzpy3.Grapher_app.Graph_Image_Module import *
from kzpy3.Localization_app.aruco_whole_room_markers import *

fail
def get_car_position_heading_validity(h5py_data_folder,graphics=False):

	L = h5r(opj(h5py_data_folder,'left_timestamp_metadata.h5py'))
	O = h5r(opj(h5py_data_folder,'original_timestamp_data.h5py'))

	left_images = O[left_image][vals][:].copy()
	left_images = left_images.mean(axis=3)
	right_images = O[right_image][vals][:].copy()
	right_images = right_images.mean(axis=3)

	if False:
		for i in range(2280,shape(left_images)[0]):
			mi(np.abs(left_images[i]-left_images[i-1]),2)
			pause(0.01)

	CA()

	pts = []
	if graphics: figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
	for k in Marker_xy_dic:
		if graphics: pts_plot(na([Marker_xy_dic[k]]))
		if is_number(k):
			txt = str(k)
			if graphics: plt.annotate(txt,Marker_xy_dic[k])
			pts.append(Marker_xy_dic[k])
			left_pt = Marker_xy_dic[(k,LEFT2)]
			right_pt = Marker_xy_dic[(k,RIGHT2)]
			if graphics: plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'b')
			left_pt = Marker_xy_dic[(k,LEFT)]
			right_pt = Marker_xy_dic[(k,RIGHT)]
			pts.append(left_pt)
			pts.append(right_pt)
			if graphics: plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
		elif graphics:
			txt = str(k[1])
			if '2' not in txt:
				plt.annotate(txt,Marker_xy_dic[k])

	pts = np.array(pts)


 
	n = [0]
	for i in range(1,shape(left_images)[0]):
		if i < len(right_images):
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			mr = np.abs(right_images[i]-right_images[i-1]).mean()
			n.append((ml+mr)/2.0)
		else:
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			n.append(ml)			


	t = O[left_image][ts][:]
	if graphics: figure('motion calculation');plot(t-t[0],n)


	hp = L[heading_pause][:]
	hp[hp<1]=0
	hp2 = 1-hp
	hp2[L[state][:]!=6] = 0

	mo_mask = L[motor][:]
	mo_mask[mo_mask<53]=0
	mo_mask[mo_mask>=53]=1.0
	o = mo_mask*hp2*n


	p=[]
	for q in o:
		if q > 0:
			p.append(q)
	if graphics: figure('motion calculation histogram');hist(p)

	o[o>(np.mean(p)+1.5*np.std(p))] = 0
	o[o<(np.mean(p)-1.5*np.std(p))] = 0
	
	if graphics: figure('motion calculation');plot(t-t[0],o)
	o_meo = na(meo(o,45))
	if graphics: plot(t-t[0],o_meo)
	#left_images=O[left_image][vals][:]
	#ctr=0
	pause_flag = False
	#dot_ctr = Timer(0.01)
	ax = na(meo(na(L[aruco_position_x][:]),45))
	ay = na(meo(na(L[aruco_position_y][:]),45))
	hx = na(meo(na(L[aruco_heading_x][:]),45))
	hy = na(meo(na(L[aruco_heading_y][:]),45))

	if graphics:
		x_min = -4.0#-(6.03/2.0)#-6.03+hw
		x_max = 4.0#(6.03/2.0)#hw
		y_min = -4.0#-(6.03/2.0)#-hw#
		y_max = 4.0#6.03/2.0#hw#
		time_counter = Timer(1/3.0)
		spause()
		raw_enter()
		cv2.destroyAllWindows()
		Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,350)
		for i in range(len(left_images)):
			time_counter.message(d2s(dp(t[i]-t[0])),'white')
			j=i+20
			if o_meo[i] >1:
				mci(O[left_image][vals][i],scale=4,title='left_image')#;spause();
				Gi[img]*=0
				Gi[ptsplot](x,pts[:,0],y,pts[:,1],color,(0,0,255))
				Gi[ptsplot](x,na([ax[j]]),y,na([ay[j]]),color,(255,255,255))
				Gi[ptsplot](x,na([hx[j]+ax[j]]),y,na([hy[j]+ay[j]]),color,(255,0,0))
				mci(Gi[img],scale=2,title='map');
				pause_flag = False
			else:
				if not pause_flag:
					mci(128+0*Gi[img],scale=2,title='map');
					pause(0.5)
					pause_flag = True
	L.close()
	O.close()
	
	return ax,ay,hx,hy,o_meo


"""



h5py_data_folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py'

runs = sggo(h5py_data_folder,'*')

for r in runs:
	if len(sggo(r,'position_data.h5py')) > 0:
		print opj(r,'position_data.h5py') + 'exists, doing nothing'

ax,ay,hx,hy,o_meo = get_car_position_heading_validity(h5py_data_folder,graphics=False)

F = h5w(opjD('temp.h5py'))
F.create_dataset('ax',data=ax)
F.create_dataset('ay',data=ay)
F.create_dataset('hx',data=hx)
F.create_dataset('hy',data=hy)
F.create_dataset('o_meo',data=o_meo)
F.close()



"""

#EOF
