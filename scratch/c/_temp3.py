
A = h5r('/home/karlzipser/Desktop/temp/h5py/Mr_Black_2017-10-24-19-54-33/aruco_position.h5py')

x = A['aruco_position_x'][:]
y = A['aruco_position_y'][:]
hx = A['aruco_heading_x'][:]
hy = A['aruco_heading_y'][:]


CA()
figure(1);clf();plt_square();xysqlim(2)
plot(x,y,',')
#plot(hx,hy,',')

for i in range(12000,13000,30/3):
	plot([x[i],hx[i]],[y[i],hy[i]],'g')
	plot(x[i],y[i],'g.')
spause()

P = h5r('/home/karlzipser/Desktop/temp/h5py/Mr_Black_2017-10-24-19-54-33/position_data.h5py')
px = P['ax'][:]
py = P['ay'][:]
phx = P['hx'][:]
phy = P['hy'][:]

D = lo('/home/karlzipser/Desktop/temp/position_dictionaries/Mr_Black_position_dictionary.pkl')
dx_ = D['ax']
dy_ = D['ay']
dhx_ = D['hx']
dhy_ = D['hy']
ts = sorted(dx_.keys())
dx,dy,dhx,dhy = [],[],[],[]
for t in ts:
	dx.append(dx_[t])
	dy.append(dy_[t])
	dhx.append(dhx_[t])
	dhy.append(dhy_[t])

figure(50);clf();plt_square();xysqlim(2)
plot(dx,dy,',')
for i in range(10000/3,13000/3,30/9):
	plot([dx[i],dx[i]+dhx[i]],[dy[i],dy[i]+dhy[i]],'r')
	plot(dx[i],dy[i],'r.')
spause()




# 23 Nov. 2017
folders = sggo('/home/karlzipser/Desktop/full_raised_observer/h5py','*')
for f in folders:
	unix_str = d2s('ln -s',f,'/home/karlzipser/Desktop/full_raised/h5py')
	print unix_str
	unix(unix_str,False)
