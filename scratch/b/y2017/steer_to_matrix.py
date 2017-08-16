


#g = zeros[30]
from scipy import signal

gaussian = signal.gaussian(301, std=6)

def sig_0to99_to_gaussian(cs,gaussian=gaussian):
	return gaussian[range(150-cs,260-cs,10)]

g_matrix = zeros((30,11))
ctr = 0
for steer in range(0,102,3):
	#clf()
	#xlim(-0.5,10.5)
	#ylim(0,1)
	g = sig_0to99_to_gaussian(steer)
	g_matrix[ctr,:] = g
	ctr += 1
	if ctr >= 30:
		break
	#plot(gaussian[range(150-steer,260-steer,10)],'o-')
	#print steer
	#pause(0.5)

