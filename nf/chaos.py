# File: chaos.py
# A simple program illustrating chaotic behavior.

from kzpy3.vis3 import *

X = []

def main(X,r):
    print("This program illustrates a chaotic function")
    x = .3#input("Enter a number between 0 and 1: ")
    for i in range(300):
        x = r * x * (1 - x)
        #x = x**2 + c
        print(x)
        X.append(x)

R = []
E = {}


for r in arange(3.5,3.8,.0003):
	figure(1);clf()
	X = []
	main(X,r)
	R.append(r)
	if not is_number(X[-1]):
		break
	E[r] = X[-32:]

	if False:
		clf()
		plot(X)
		plt.xlabel(dp(r))
		spause()
	#raw_enter()

figure(2);clf()

for r in E.keys():
	plot(r*(zeros(32)+1),E[r],'k.',markersize=2)#,m=2)
ylim(0,1)

raw_enter()