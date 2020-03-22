from kzpy3.vis3 import *

clf();spause()
L = {}
for j in range(30000-1000,30000+1000,10):
	print j
	L[j] = []
	for i in range(30000-1000,30000+1000):
		s = measure.compare_ssim(Q['normal'][i],Q['normal'][j],multichannel=True)
		L[j].append(s)
	plot(L[j]);spause()
	print(j,na(L[j]).mean())
