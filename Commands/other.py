from kzpy3.utils3 import *

timer = Timer(0.1)

raw_enter(' other.py ')

while True:
	if timer.check():
		timer.reset()
		soD('a',{'one':rndn(3),'two':rndint(100)})
	else:
		time.sleep(0.01)
		continue