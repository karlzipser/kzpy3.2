from kzpy3.vis import *
import threading

class B:
    def __init__(self):
    	self.dic = {}

b = B()

plt.ion()
ctr = {}
ctr[0]=0
ctr[1]=1

def add(b,key,delay):
	global ctr
	t0 = time.time()
	while time.time()-t0 < 10:
		ctr[key] += 1
		b.dic[key] = np.random.random(1)
		#print 'added'
		time.sleep(delay)

black = threading.Thread(target=add,args=(b,0,0.5))
black.start()
white = threading.Thread(target=add,args=(b,1,0.3))
white.start()

t0 = time.time()
while time.time()-t0 < 10:
	#b.dic[3] = 0.5
	#print 'did it'
	time.sleep(0.1)
pprint(ctr)

# 3pm on 7th Monday