from kzpy3.utils2 import *
import threading

STOP = False

def simple_thread(c):
	global STOP
	timer = Timer(1)
	while True:
		if STOP == True:
			break
		timer.message(d2s('thread',c))
		time.sleep(1)

ctr = 0
while True:
	threading.Thread(target=simple_thread,args=[ctr]).start()
	ctr += 1
	time.sleep(0.1)



from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()


 