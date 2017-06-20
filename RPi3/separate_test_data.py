from kzpy3.utils import *

rgb_runs_path = opj('Desktop/RPi3_data/runs_scl_100_RGB')
bw_runs_path = opj('Desktop/RPi3_data/runs_scale_50_BW')

_,rgb_runs = dir_as_dic_and_list(rgb_runs_path)

_,bw_runs = dir_as_dic_and_list(bw_runs_path)

for i in range(len(rgb_runs)):
	assert(rgb_runs[i].split('scl')[0] == bw_runs[i].split('scl')[0])

rnd_inx = []
temp_inx_lst = range(len(rgb_runs))
for i in range(int(0.15*len(rgb_runs))):
	indx = temp_inx_lst[np.random.randint(len(temp_inx_lst))]
	rnd_inx.append(indx)
	temp_inx_lst.remove(indx)

print rnd_inx

print d2s('mkdir -p',rgb_runs_path+'_test')
print d2s('mkdir -p',bw_runs_path+'_test')

for r in rnd_inx:
	print(d2s('mv',opj(rgb_runs_path,rgb_runs[r]),rgb_runs_path+'_test'))
	print(d2s('mv',opj(bw_runs_path,bw_runs[r]),bw_runs_path+'_test'))

"""
mkdir -p Desktop/RPi3_data/runs_scl_100_RGB_test
mkdir -p Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/10Feb16_08h31m21s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/10Feb16_08h31m21s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/14Feb16_17h07m47s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/14Feb16_17h07m47s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_14h53m10s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/09Feb16_14h53m10s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/27Feb16_09h56m16s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/27Feb16_09h56m16s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/21Feb16_10h01m38s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/21Feb16_10h01m38s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/13Feb16_08h36m56s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/13Feb16_08h36m56s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/23Feb16_15h46m09s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/23Feb16_15h46m09s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/23Feb16_11h49m16s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/23Feb16_11h49m16s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_14h10m21s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/09Feb16_14h10m21s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/23Feb16_15h36m56s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/23Feb16_15h36m56s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/25Feb16_16h31m35s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/25Feb16_16h31m35s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/11Feb16_13h37m13s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/11Feb16_13h37m13s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/13Feb16_08h36m56s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/13Feb16_08h36m56s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/09Feb16_14h03m20s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/09Feb16_14h03m20s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/14Feb16_10h23m59s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/14Feb16_10h23m59s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/26Feb16_10h30m26s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/26Feb16_10h30m26s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/14Feb16_12h37m05s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/14Feb16_12h37m05s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/14Feb16_17h33m13s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/14Feb16_17h33m13s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/10Feb16_08h38m32s_scl=100_mir=1 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/10Feb16_08h38m32s_scl=50_mir=1 Desktop/RPi3_data/runs_scale_50_BW_test
mv Desktop/RPi3_data/runs_scl_100_RGB/27Feb16_10h10m31s_scl=100_mir=0 Desktop/RPi3_data/runs_scl_100_RGB_test
mv Desktop/RPi3_data/runs_scale_50_BW/27Feb16_10h10m31s_scl=50_mir=0 Desktop/RPi3_data/runs_scale_50_BW_test
"""






from kzpy3.utils import *

bw_runs_path = opj('Desktop/RPi3_data/runs_scale_25_BW')

_,bw_runs = dir_as_dic_and_list(bw_runs_path)

rnd_inx = []
temp_inx_lst = range(len(bw_runs))
for i in range(int(0.20*len(bw_runs))):
	indx = temp_inx_lst[np.random.randint(len(temp_inx_lst))]
	rnd_inx.append(indx)
	temp_inx_lst.remove(indx)

print rnd_inx

print d2s('mkdir -p',bw_runs_path+'_test')

for r in rnd_inx:
	print(d2s('mv',opj(bw_runs_path,bw_runs[r]),bw_runs_path+'_test'))

"""
mv Desktop/RPi3_data/runs_scale_25_BW/09Feb16_13h33m51s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/10Feb16_09h15m53s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/10Feb16_13h31m38s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/23Feb16_11h49m16s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/13Feb16_08h36m56s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/14Feb16_10h23m59s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/25Feb16_16h31m35s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/09Feb16_13h54m07s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/10Feb16_13h12m56s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/10Feb16_08h52m06s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/27Feb16_10h10m31s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/24Feb16_11h11m10s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/11Feb16_16h37m17s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/26Feb16_13h18m36s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/13Feb16_08h47m41s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/26Feb16_13h03m12s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/26Feb16_12h42m51s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/24Feb16_14h20m48s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/23Feb16_15h56m00s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/09Feb16_13h54m07s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/09Feb16_14h27m57s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/27Feb16_10h21m52s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/13Feb16_08h36m56s_scl=25_mir=0 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/25Feb16_17h01m59s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/10Feb16_08h56m14s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/25Feb16_16h47m36s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
mv Desktop/RPi3_data/runs_scale_25_BW/24Feb16_14h20m48s_scl=25_mir=1 Desktop/RPi3_data/runs_scale_25_BW_test
"""
