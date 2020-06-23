# To run, type python kzpy3/nf/eg0.py in terminal

from kzpy3.vis3 import *




a,b,c = 0,20,1

zn1=0

graphics = True

C = -1

def f( x ):
	y = x * x
	return y

def __g( zn ):
	zn1 =zn*zn+C
	return zn1


def g( zn ):
	zn1 =zn*zn+C
	return zn1

def h(x,q):
	if q > 10:
		return x
	y = h(x * x, q+1) + C
	clp(y,p=0)
	return y

def print_XY( X, Y ):
	clp('X:', '`', X, '`wg')
	clp('Y:', '`',Y,'`gw', '\n', p=0.)


for C in arange(0.01,1,0.02):

	X,Y = [],[]

	for x in range( a, b, c ):
		print_XY( X, Y )
		X.append( x )
		zn=zn1
		zn1 = h(zn,0)
		Y.append( zn1 )


	if graphics:
		clf() # clear plot
		#plt_square()  # make aspect ratio one.
		plot(X[10:], Y[10:], 'co')
		plot(X[10:], Y[10:], 'r:')
		plt.xlabel('X')
		plt.ylabel('Y')
		spause() # makes the current plot visible


	print_XY( X, Y )

	raw_enter()

#EOF


