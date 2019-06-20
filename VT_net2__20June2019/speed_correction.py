from kzpy3.vis3 import *

from scipy.optimize import curve_fit


def fit_func(x, m, b):
    return m*x + b





data = na([
	[5.33,1.75],
	[5.74,1.9],

	[5.76,0.9],
	[5.89,1.05],
	[5.71,1.1],

	[5.81,0.72],

	[4.64,0.37],
	[4.99,0.46],
	[4.03,0.25],
	[3.74,0.24],
])

dist = data[:,0]
vel = data[:,1]

params = curve_fit(fit_func, vel[-5:], dist[-5:])
[m, b] = params[0]

x = arange(0,2,.01)
y = fit_func(x,m,b)

# m = 4.078
# b = 2.978

def non_linear_fit(vel):
	q = fit_func(vel,m,b)
	if q > 5.75:
		return 5.75
	elif q < 0:
		return 0
	else:
		return q
	"""
	if vel < 0.22:
		return non_linear_fit(0.22)
	elif vel > 0.68:
		return non_linear_fit(0.68)
	else:
		return fit_func(vel,m,b)
	"""

def non_linear_correction(vel):
	return 5.75/non_linear_fit(vel)

vel_ = list(x)
dist_ = []
dist_c = []
for v in vel_:
	dist_.append(non_linear_fit(v))
	dist_c.append(non_linear_correction(v))

dist_cor = []
for v,d in zip(vel,dist):
	dist_cor.append(d*non_linear_correction(v))

CA()
plot(vel_,dist_,'c.')
plot(vel_,dist_c,'r.')

plot(vel,dist,'ko')
plot(vel,dist_cor,'ro')
