from kzpy3.vis import *
import kzpy3.teg9.working.get_data_with_hdf5 as get_data_with_hdf5
import caffe

REPO = 'kzpy3'
TEG = 'teg9'
CAF = 'caf8'
DISPLAY = True

ignore = ['reject_run','left','out1_in2','Smyth','racing'] # runs with these labels are ignored
require_one = [] # at least one of this type of run lable is required
use_states = [1]

if False:
	MODEL = 'z2_color'
	bair_car_data_path = opjD('bair_car_data_new') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	#weights_file_path =  most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))))
	#weights_file_path = opjh('caffe_models/z2_color.caffemodel')
	weights_file_path = None
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1

if True:
	MODEL = 'z3_color'
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	#weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	weights_file_path = opj('caffe_models/z3_color_iter_700000.caffemodel')
	N_FRAMES = 3 # how many timesteps with images.
	N_STEPS = 30 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z1_color'
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	N_FRAMES = 1 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1







"""
if gpu >= 0:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

import_str = "import REPO.CAF.MODEL.solver as Solver"
import_str = import_str.replace("REPO",REPO)
import_str = import_str.replace("CAF",CAF)
import_str = import_str.replace("MODEL",MODEL)
exec(import_str)

if weights_file_path:
	print(d2s("Copying weights from",weights_file_path,"to",Solver.solver))
	Solver.solver.net.copy_from(weights_file_path)
else:
	print(d2s("No weights loaded to",Solver.solver))
"""

hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')
"""
print_timer = Timer(15)
loss10000 = []
loss = []
rate_timer_interval = 10.
rate_timer = Timer(rate_timer_interval)
rate_ctr = 0
"""
get_data_with_hdf5.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)


steer_dic = {}
print('\nloading low_steer... (takes awhile)')
steer_dic['low'] = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
print('\nloading high_steer... (takes awhile)')
steer_dic['high'] = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))


for Q in ['low','high']:
	print Q
	print_stars()
	#hdf5_filename = opj('/media/karlzipser/SSD_2TB_Ext4',MODEL+'_'+Q+'_Nothing_steer_data.hdf5')
	#h5py_file = h5py.File(hdf5_filename,'w')
	ctr = 0
	ctr2 = 0
	timer = Timer(0)
	meta = {}
	while ctr < len(steer_dic[Q]):
		choice = steer_dic[Q][ctr]
		run_code = choice[3]
		seg_num = choice[0]
		offset = choice[1]
		data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,use_states=use_states)
		#data = None
		if data != None:
			"""
			grp = h5py_file.create_group(str(ctr))
			grp['right'] = data['right'][:].astype('uint8')
			grp['left']  = data['left'][:].astype('uint8')
			meta[ctr] = {}
			meta[ctr]['name']  = data['name']
			meta[ctr]['labels']  = data['labels']
			meta[ctr]['states']  = data['states']
			meta[ctr]['steer']  = data['steer']
			meta[ctr]['motor']  = data['motor']
			"""
			print ctr2
			ctr2 += 1
		ctr += 1
		#if ctr > 100:
		#	break
		if np.mod(ctr2,100) == 0:
			print ctr2/timer.time()
	#h5py_file.close()
	#save_obj(meta,hdf5_filename.replace('.hdf5','.pkl'))