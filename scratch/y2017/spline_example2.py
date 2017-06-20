# In this example the cubic spline is used to interpolate a sampled sinusoid.
# You can see that the spline continuity property holds for the first and
# second derivatives and violates only for the third derivative.
import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline

import matplotlib.pyplot as plt



n = 10
M=[]
X=[]
for i in range(n/2,len(L),n):
	M.append(L[i-n/2:i+n/2,1].mean())
	X.append(i)
M = array(M)
X = array(X)
x = X #np.arange(len(M))
y = M
cs = CubicSpline(x, y)
xs = np.arange(X[0],X[-1],1)
plt.figure(figsize=(6.5, 4))
plt.plot(L[:,0], label='data')
plt.plot(x, y, 'o', label='smoothed data')
plt.plot(xs, cs(xs), label="S")
plt.legend(loc='lower left', ncol=2)
plt.show()


import scipy.interpolate
CubicSpline = scipy.interpolate.CubicSpline

data = array(Bul['pts'])[:,0]
time_points = array(Bul['pts'])[:,2]

def get_cubic_spline(time_points,data,n=20):
	n = 10
	D = []
	T = []
	for i in range(n/2,len(time_points),n):
		D.append(data[i-n/2:i+n/2].mean())
		T.append(time_points[i-n/2:i+n/2].mean())
	D,T = array(D),array(T)
	cs = CubicSpline(T,D)
	new_time_points = np.arange(time_points[0],time_points[1],1)
	plot(time_points,data,'o')
	plot(T,D,'o', label='smoothed data')
	plot(time_points,cs(time_points),label="S")
	plt.legend(loc='lower left', ncol=2)
	return cs



