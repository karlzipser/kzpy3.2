from kzpy3.utils3 import *

timer = Timer(10)

ctr = 0
while not timer.check():
	a = rndn(1000,1000)
	#cb('	a = rndn(1000,1000)')
	b = rndn(1000,1000)
	#cb('	b = rndn(1000,1000)')
	a = a * b
	#cb('	a = a * b')
	a += b
	#cb('	a += b')
	l = []
	for i in range(1000):
		l.append(rnd(1))
	#cb('	l.append(rnd(1))')
	ctr += 1
	#cb('ctr =',ctr)
cg('ctr =',ctr)