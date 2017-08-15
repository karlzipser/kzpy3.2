figure(5);clf();plt_square();xysqlim(2.1*107.0/100.0);
rpts_ = []
for k_ in Marker_xy_dic.keys():
	if not is_number(k_):
		if k_[1] == right:
			rpts_.append(Marker_xy_dic[k_])
rpts_ = na(rpts_)
pts_plot(rpts_,'r')

lpts_ = []
for k_ in Marker_xy_dic.keys():
	if not is_number(k_):
		if k_[1] == left:
			lpts_.append(Marker_xy_dic[k_])
lpts_ = na(lpts_)
pts_plot(lpts_,'b')




current_position_ = na((0.0,0.0))
#d_current_position_ = na((0,-0.01))
d_theta_ = 0.01
theta_ = 0.1

for i_ in range(200):
	clf();plt_square();xysqlim(2.1*107.0/100.0);
	current_position_ += d_current_position_
	theta_ += d_theta_
	rpts2_ = rpts_ - current_position_
	rpts2_ = na(rotatePolygon(rpts2_,theta_)) + current_position_ + d_current_position_
	
	pts_plot(lpts2_,'b')
	plot([0,0],[0,0.1],'k')
	print(theta_,current_position_)
	pause(0.0001)



pts = rpts_.copy()

xy_ = na((0.0,0.0))
theta_ = 0
for i_ in range(200):
	if i_ < 100:
		theta_ += 0.5
	else:
		theta_ -= 0.5
	xy_ += na(rotatePoint((0,0),(0,0.01),theta_))
	pts_pov_ = na(rotatePolygon(pts_-xy_,-theta_))
	clf();plt_square();xysqlim(2.1*107.0/100.0);pts_plot(pts_pov_,'b');plot(0,0,'ok');pause(0.001)
	#cf();plt_square();xysqlim(2.1*107.0/100.0);pts_plot(pts_,'b');plot(xy_[0],xy_[1],'ok');pause(0.001)
	print dp(theta_)


d = []
b = []
for a in arange(-45,45):
	b.append(a)
	d.append(1.0+(np.abs(a/45.0)**2)/10.0)
clf();plot(b,d,'o')











n = []
for i in rlen(hmx):
	n.append(angle_clockwise((0,1),(hmx[i]-Aruco_trajectories[left][x][i],hmy[i]-Aruco_trajectories[left][y][i])))
"""	
for i in range(0,len(hmx),5):
	clf();plt_square();xysqlim(3);
	plot(Aruco_trajectories[left][x][i],Aruco_trajectories[left][y][i],'.');pause(0.001)
	print n[i]
"""
figure(6);
for an in range(15,180+15,30):
	ox=[];oy=[]
	clf();plt_square();xysqlim(2*107.0/100.0)
	for i in range(0,len(hmx),5):
		if n[i] >an-15 and n[i]<an+15:
			ox.append(Aruco_trajectories[left][x][i])
			oy.append(Aruco_trajectories[left][y][i])
			plot(ox[-1],oy[-1],'r.');spause()



ox0=ox;oy0=oy






