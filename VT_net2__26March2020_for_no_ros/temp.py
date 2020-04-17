#,a
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
#,b

#EOF
