from kzpy3.utils import *

t1 = time.time()
a = zeros((1000,1000))

for i in range(1000):
	a = a*a

print time.time()-t1