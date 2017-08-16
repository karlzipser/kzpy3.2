from kzpy3.utils import *


f = open(opjD('temp.txt'), 'w')
t0 = time.time()
for i in range(1000):
    print i
    f.write(d2s(i,'\n'))
    #time.sleep(0.001)
print time.time()-t0