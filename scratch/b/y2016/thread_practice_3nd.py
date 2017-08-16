from kzpy3.vis import *
import threading
from Queue import *

class B:
    def __init__(self):
    	self.dic = {}

b = B()

plt.ion()
ctr = {}
ctr[0]=0
ctr[1]=1

def process_1(q,n):
	global ctr
	t0 = time.time()
	while time.time()-t0 < 10:
		ctr[0] += 1
		q.put(1)
		time.sleep((np.random.random(1)/20.)[0])

def process_2(q,n):
	global ctr
	t0 = time.time()
	while not q.empty(): #while time.time()-t0 < 10:
		#if q.qsize() > 1:
		m = q.get()
		ctr[1] += 1
		time.sleep((np.random.random(1)/20.)[0])

q = Queue()
black = threading.Thread(target=process_1,args=(q,1))
black.start()
white = threading.Thread(target=process_2,args=(q,2))
white.start()

t0 = time.time()
while time.time()-t0 < 20:
	print(q.qsize())
	time.sleep(0.1)
pprint(ctr)

# 3pm on 7th Monday