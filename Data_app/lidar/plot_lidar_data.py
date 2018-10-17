###start
from kzpy3.vis3 import *
figure(2);clf()
plt_square()
xylim(-5,5,-5,5)
P = lo(opjD('P'))
O = na(P)
O = O[:,:2]
pts_plot(O,color='k',sym=',')
"""
for i in rlen(P):
	if np.mod(i,1000) == 0:
		spause()
		print i
	xyz = P[i]
	plot(xyz[0],xyz[1],',')
"""
raw_enter()
###stop