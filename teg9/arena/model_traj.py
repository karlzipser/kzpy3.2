

X=traj['left']['x']
Y=traj['left']['y']

offset = 5000
interval = 5*30
theta = 90
n = 10
x = X[offset:offset+interval]
y = Y[offset:offset+interval]

xya = array(zip(x,y))

figure(1)
clf()
plt_square()
xylim(-5,5,-5,5)
axy -= axy[:n,:].mean(axis=0)
theta = angle_clockwise([0,1],normalized_vector_from_pts(axy[:n]))

xy = zip(axy[:,0],axy[:,1])

xyr = []
for pt in xy:
	xyr.append(rotatePoint([0,0],pt,theta))

pts_plot(axy,'b')
pts_plot(array(xyr))

dx = []
dy = []
for i in range(1,len(xyr)):
	dx.append(xyr[i][0]-xyr[i-1][0])
	dy.append(xyr[i][1]-xyr[i-1][1])