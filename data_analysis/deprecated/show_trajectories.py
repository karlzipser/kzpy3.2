from kzpy3.vis import *
from kzpy3.data_analysis.trajectory_generator.evasion_generator import *
CS = lo(opjh('kzpy3/teg9/trajectories.pkl'))

figure('top')
t1 = 1493425694.71+5
t2 = 1493425899.676476 - 100
timestamps = np.arange(t1,t2,1/30.)

CA()
figure('top',figsize=(6,6))

car = 'Mr_Black'
side = 'left'
own_xy = []

for t in timestamps:
	x = CS[car][side][0](t)
	y = CS[car][side][1](t)
	own_xy.append([float(x),float(y)])

car = 'Mr_Blue'
other_xys = []

for t in timestamps:
	x = CS[car][side][0](t)
	y = CS[car][side][1](t)
	other_xys.append([float(x),float(y)])

#own_xy,other_xy,timestep_start, timesteps_ahead
#get_evasive_trajectory(own_xy,other_xys,1929, 200,1.5)
get_evasive_trajectory(own_xy,other_xys,1925, 5, 5)



# collision timestamps# 1929
# 1930
# 1931
# 1932
# 1933
# 1934
# 1935
# 1936
# 1937
# 1938
# 1939
# 1940
# 1941
# 1942
# 1943
# 1944
# 1945
# 1946
# 1947
# 1948
# 1949
# 1950
# 1951
# 1952
# 1965
# 1966
# 1967
# 1968
# 1969
# 1970
# 1971
# 1972