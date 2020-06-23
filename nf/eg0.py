from kzpy3.vis3 import *

x = []
y = []

a = -5
b = 5+1 # why +1?
c = 1


def f(x):
	y = x * x
	return y



for i in range(a, b, c):
	x.append( i )
	y.append( f( i ) )




clf() # clear plot
plt_square()  # make aspect ratio one.

plot(x, y, 'o-')

spause() # makes the current plot visible


clp('x:', x)
clp('y:', y, r=1)

