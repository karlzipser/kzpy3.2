# To run, type python kzpy3/nf/eg0.py in terminal

from kzpy3.vis3 import *


X,Y = [],[]

a,b,c = -5,6,1

graphics = True


def f( x ):
	y = x * x
	return y


def print_XY( X, Y ):
	clp('X:', '`', X, '`wb')
	clp('Y:', '`',Y,'`bw', '\n', p=1/2.)


for x in range( a, b, c ):
	print_XY( X, Y )
	X.append( x )
	Y.append( f( x ) )


if graphics:
	clf() # clear plot
	plt_square()  # make aspect ratio one.
	plot(X, Y, 'o-')
	plt.xlabel('X')
	plt.ylabel('Y')
	spause() # makes the current plot visible


print_XY( X, Y )

raw_enter()

#EOF
