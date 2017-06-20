from kzpy3.vis import *
import threading

class B:
    def __init__(self):
    	self.data = np.zeros((100,100))+0.5

b = B()

plt.ion()

def draw(img,color,delay):
	t0 = time.time()
	while time.time()-t0 < 100:
		X,Y = shape(img)
		x = np.random.randint(X)
		y = np.random.randint(Y)
		img[x,y] = color
		#plt.figure(1)
		#plt.clf()
		#mi(img)
		#print 'sleeping'
		time.sleep(delay)

black = threading.Thread(target=draw,args=(b.data,0,0.3))
black.start()
white = threading.Thread(target=draw,args=(b.data,1,0.01))
white.start()

t0 = time.time()
while time.time()-t0 < 100:
	mi(b.data)
	plt.pause(0.2)
