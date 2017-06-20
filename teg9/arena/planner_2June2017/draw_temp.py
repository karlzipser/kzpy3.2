from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *

R = 4*107/100.0

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def f(x,a,b,c,d,e):
	if is_number(x):
		x = array([x])
	g = c*gaussian(x/R,0,d)
	ga = c*gaussian(a,0,d)
	y = 0*x
	for i in range(len(x)):
		if x[i]/R < -a:
			y[i] = (x[i]/R+a)**2 / b
		elif x[i]/R > a:
			y[i] = (x[i]/R-a)**2 / b
		else:
			y[i] = g[i] - ga
	y = (1-e)*y + e
	return y







x = arange(-R,R+0.01,0.01)

clf();xylim(0,2*R,0,1)

for m in ['direct','furtive','play','follow']:
	if m == 'direct':
		a = 0.75
		b = (-1+a)**2
		c = 0.75
		d = 1/2.0
		e = 0
	if m == 'furtive':
		a = 0.93
		b = (-1+a)**2
		c = 1.0
		d = 1/1.5
		e = 0
	if m == 'play':
		a = 0.0
		b = (-1+a)**2
		c = 0.0
		d = 1/2.0
		e = 0
	if m == 'follow':
		a = 0.0
		b = (-1+a)**2
		c = 0.0
		d = 1/2.0
		e = 0.5

	y = f(x,a,b,c,d,e)
	for i in range(len(y)):
		if y[i] < 0.1:
			yi = 0
			for d in [-3,-2,-1,1,2,3]:
				yi += y[i+2*d]
			yi /= 6.0
			y[i] = yi
	plot(x+R,y,'.-');pause(0.01)

"""

"""

"""


def f1(x):
	if is_number(x):
		x = array([x])
	y = 0*x
	for i in range(len(x)):
		y[i] = (np.cos(pi*x[i])+1)/4.0
		if abs(x[i]) > 1.5:
			y[i] += 0.08
	return y


def f4(x):
	if is_number(x):
		x = array([x])
	y = 0*x
	for i in range(len(x)):
		f = (1.0+abs(x[i]/0.1))/25.0
		#a = 10.0+abs(x[i])/10.0
		a=1.0
		#y[i] = (a*np.cos(f*pi*x[i])+1)/4.0
		y[i] = a*np.cos(f*pi*x[i])
	y = z2o(y)
	amin = np.argmin(y)
	if amin > len(y)/2:
		amin = len(y)-amin
	print amin
	q = 5
	v = 0.5
	y[:amin] *= q
	y[-amin:] *= q
	y[amin:-amin] *= v


	return y

def f2(x):
	return x**2+1
	#return (1.0-np.cos(x/2.0))/2+0.25
def f3(x):
	return f1(x)*f2(x)

figure(1)
clf()
plot(x,f4(x),'b.-')
#plot(x,f2(x),'k')
#plot(x,f3(x),'r')

if True:
	img = zeros((100,100))
	for X in range(shape(img)[0]):
		for Y in range(shape(img)[0]):
			x_ = -50*(X-shape(img)[0]/2.0)/(1.0*shape(img)[0])
			y_ = -50*(Y-shape(img)[0]/2.0)/(1.0*shape(img)[0])
			r = length([x_,y_])
			img[X,Y] = f(r)
	mi(img,2)


figure(3);clf();plot(img[shape(img)[0]/2,:])

pause(0.001)

"""