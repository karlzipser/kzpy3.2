folders = sggo('/media/karlzipser/rosbags/Mr_Orange_30August2017/new/*')

ctr = 1
for f in folders:
    print f
    new_name = d2n('Mr_Orange_30August2017_',ctr)
    new_f = opj(pname(f),new_name)
    print new_f
    ctr += 1
    unix(d2s('mv',f,new_f))



f=h5r('/media/karlzipser/ExtraDrive2/demo_data/bdd_aruco_demo_3Sept2017/h5py/Mr_Yellow_2017-09-03-09-08-56/original_timestamp_data.h5py')


for i in range(2280,shape(l)[0]):
	mi(np.abs(l[i]-l[i-1]),2)
	pause(0.01)



from kzpy3.Grapher_app.Graph_Image_Module import *
pts = []
figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
for k in Marker_xy_dic:
	pts_plot(na([Marker_xy_dic[k]]))
	if is_number(k):
		txt = str(k)
		plt.annotate(txt,Marker_xy_dic[k])
		pts.append(Marker_xy_dic[k])
		left_pt = Marker_xy_dic[(k,LEFT2)]
		right_pt = Marker_xy_dic[(k,RIGHT2)]
		plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'b')
		left_pt = Marker_xy_dic[(k,LEFT)]
		right_pt = Marker_xy_dic[(k,RIGHT)]
		pts.append(left_pt)
		pts.append(right_pt)
		plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
	else:
		txt = str(k[1])
		if '2' not in txt:
			plt.annotate(txt,Marker_xy_dic[k])

pts = np.array(pts)


l=f[left_image][vals][:] 
l=l.mean(axis=3) 
n = []
for i in range(1,shape(l)[0]):
	m = np.abs(l[i]-l[i-1]).mean()
	n.append(m)

t=f[left_image][ts][:] 
CA();plot(n) 

t=f[left_image][ts][:] 
CA();plot(t[1:]-t[1],n)


L = h5r('/media/karlzipser/ExtraDrive2/demo_data/bdd_aruco_demo_3Sept2017/h5py/Mr_Yellow_2017-09-03-09-08-56/left_timestamp_metadata.h5py')

hp=L[heading_pause][:]
hp[hp<1]=0
hp2=1-hp

mo_mask = L[motor][:]
mo_mask[mo_mask<53]=0
mo_mask[mo_mask>=53]=1.0

o=mo_mask*hp2*n

p=[]
for q in o:
	if q > 0:
		p.append(q)
figure(5);hist(p)

o[o>(np.mean(p)+2*np.std(p))] = 0
o[o<(np.mean(p)-2*np.std(p))] = 0
o_meo = meo(o,45)
l=f[left_image][vals][:]
ctr=0
pause_flag = False
dot_ctr = Timer(0.01)
ax = meo(na(L[aruco_position_x][:]),45)
ay = meo(na(L[aruco_position_y][:]),45)
hx = meo(na(L[aruco_heading_x][:]),45)
hy = meo(na(L[aruco_heading_y][:]),45)


Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,350)
for i in range(len(l)):
	j=i+20
	if True:#try:
		if o_meo[i] >1:
			mci(l[i],scale=4)#;spause();
			if True:#dot_ctr.check():
				#figure(1);clf();plt_square();xysqlim(4);plot(ax[j],ay[j],'r.');plot(hx[j]+ax[j],hy[j]+ay[j],'b.');
				#pts_plot(pts)
				#spause()
				#dot_ctr.reset()
				x_min = -4.0#-(6.03/2.0)#-6.03+hw
				x_max = 4.0#(6.03/2.0)#hw
				y_min = -4.0#-(6.03/2.0)#-hw#
				y_max = 4.0#6.03/2.0#hw#

				Gi[img]*=0
				Gi[ptsplot](x,pts[:,0],y,pts[:,1],color,(0,0,255))
				Gi[ptsplot](x,na([ax[j]]),y,na([ay[j]]),color,(255,255,255))
				Gi[ptsplot](x,na([hx[j]+ax[j]]),y,na([hy[j]+ay[j]]),color,(255,0,0))
				mci(Gi[img],scale=2,title='map');
			pause_flag = False
		else:
			if not pause_flag:
				pause(0.5)
				pause_flag = True
	#except:
	#	pass




