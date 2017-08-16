from kzpy3.utils import *
import threading
ctr = 0
def worker():
	global ctr
	ctr += 1
	while ctr < 100:
		print(d2s(ctr,'worker'))
		time.sleep(0.5)
	return

threads = []
for i in range(5):
	t = threading.Thread(target=worker)
	threads.append(t)
	t.start()

for j in range(100):
	ctr += 1
	time.sleep(0.5)  