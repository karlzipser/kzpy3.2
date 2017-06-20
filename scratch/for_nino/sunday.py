"""
from kzpy3.vis import *

n = 100
M = np.zeros((n,n))

for x in range(n):
	for y in range(n):
		M[x,y] = x+y

mi(M)

print "hit enter to quit"
raw_input()

"""



from kzpy3.vis import *

n = 100
M = np.zeros((n,n))

for x in range(n):
	for y in range(n):
		M[x,y] = x+y

mi(M)

print "hit enter to quit"
raw_input()