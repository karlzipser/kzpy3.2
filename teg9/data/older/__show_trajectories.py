from kzpy3.vis import *

CS = lo(opjh('kzpy3/teg9/trajectories.pkl'))

figure('top')
t1 = 1493425694.71+5
t2 = 1493425899.676476 - 100
T = np.arange(t1,t2,1/30.)

CA()
figure('top',figsize=(6,6))
for car in ['Mr_Black','Mr_Blue']:
	for side in ['left','right']:
		x = CS[car][side][0](T)
		y = CS[car][side][1](T)
		plot(x,y,'.')
