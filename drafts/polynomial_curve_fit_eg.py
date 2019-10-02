#,a

from vis3 import *

m = 3
x = arange(0,m,m/30.)
y = np.sin(2*np.pi*x) + 0.25*rndn(len(x))

clf()

plt.plot(x,y,'ok')

for n in range(1,12,1):
	raw_enter(d2s("n =",n," "))
	z = np.polyfit(x, y, n)
	f = np.poly1d(z)

	x_new = np.linspace(x[0], x[-1], 50)
	y_new = f(x_new)

	plt.plot(x_new, y_new)
	spause()

#,b