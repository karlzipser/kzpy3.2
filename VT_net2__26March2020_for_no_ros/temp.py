
from kzpy3.vis3 import *

def plot_line(A,B,c='r'):
	plot([A[0],B[0]],[A[1],B[1]],c)

A = (1,1)
B = (-2,1.5)
D = (0,3)
E = (-4,4)

def slope(A,B):
	dy = B[1] - A[1]
	dx = B[0] - A[0]
	return dy/(1.0*dx)

def y_intercept(A,m):
	b = A[1] - m * A[0]
	return b

def test_line(m,b,x0,x1,c=':'):
	A = (x0,m*x0+b)
	B = (x1,m*x1+b)
	plot_line(A,B,c)


def get_xy(A,B,D,E,show=True):
	mAB = slope(A,B)
	bAB = y_intercept(A,mAB)

	mBC = -1/mAB
	bBC = y_intercept(B,mBC)

	mDE = slope(D,E)
	bDE = y_intercept(D,mDE)

	x = (bDE - bBC) / (mBC - mDE)

	y = mBC * x + bBC

	if show:
		figure(1)
		clf()
		plt_square()
		xysqlim(5)

		plot_line(A,B,'r.-')
		plot_line(D,E,'c.-')

		test_line(mAB,bAB,-10,10)

		test_line(mBC,bBC,-10,10)

		test_line(mDE,bDE,-10,10)

		plot(x,y,'ok')

		spause()

	return x,y


x,y = get_xy(A,B,D,E)
print dp(x),dp(y)



import __main__ as main
if hasattr(main, '__file__'):
	cm('Done.',ra=1)

#, a
aa = []
ra = []
figure(1)
clf()
plt_square()
for a in range(360):
	r = np.radians(a)
	x = np.cos(r)
	y = -np.sin(r)
	plot(x,y,'.')
	b = angle_clockwise((1,0),(x,y)) + 3*rndn()
	aa.append(a)
	ra.append(b)
figure(2)
clf()
plot(aa)
plot(ra)
spause()
#,b

#,a
aa = []
ra = []
rb = []

for m in np.concatenate((arange(-10,10,0.1),arange(-.001,.001,0.0001))):
	x = 1
	y = m
	if x >= 0 and y >= 0:
		
	b = angle_clockwise((1,0),(x,y)) + 1*rndn()
	aa.append(m)
	ra.append(b)
	if m > 0:
		rb.append(b-360)
	else:
		rb.append(b)
rb = -na(rb)
figure(1)
clf()
#plot(aa)
plot(aa,ra,'.')
plot(aa,rb+10,'.')
spause()
#,b

#EOF
