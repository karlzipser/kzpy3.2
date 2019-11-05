
from kzpy3.vis3 import *

D = lo(opjD('Data','Network_Predictions','tegra-ubuntu_29Oct18_13h28m05s.net_predictions.pkl'))

# keys = ['index', 'right', 'direct', 'ts', 'run_name', 'left']

run = 'tegra-ubuntu_29Oct18_13h28m05s'
O = h5r(opjD('Data',
	'1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations/local/left_direct_stop/h5py',
	run,
	'original_timestamp_data.h5py'
	))


start = 25000
end = len(D['index'])
step = 2
for i in range(start,end,step):
	
	clf()
	xlim(-45,45)
	for a in [('left','r'),('direct','b'),('right','g')]:
		for j in range(-3,0):
			plot(-D[a[0]][i+j]['heading'],range(10),a[1]+'.-')
	plt.title(d2s(i))
	spause()
	mci(O['left_image']['vals'][i],delay=1,scale=3.0,title=run)
	


#EOF
