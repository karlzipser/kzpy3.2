from kzpy3.caf6.cafutils import *
from kzpy3.caf6.Caffe_Net import *
from kzpy3.caf6.protos import *

##############################################################################
##############################################################################
##############################################################################
#
model_path = opjh("kzpy3/caf6/z2_color_crop")
version = 'version 1b'
gpu = 1
base_lr = 0.005
snapshot = 100000
to_require=['snow']
to_ignore=['left']
restore_solver = False
train_time_limit = None # None means no time  limit
test_time_limit = None #30 # None means no time  limit
weights_file_mode = None # 'most recent' # 'this one' #None #'most recent' #None #'most recent'
weights_file_path =  None # opjD(fname(model_path)) #opjD('z2_color_trained_12_15_2016') #opjD('z2_color_long_train_21_Jan2017') #None #opjh('kzpy3/caf6/z2_color/z2_color.caffemodel') #None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')
runs_folder = opjD('bair_car_data_new','hdf5','runs')
test_runs_folder = opjD('bair_car_data','hdf5','test_runs')

TRAIN = True

train_val_lst = [
	d2s('#',model_path),
	d2s('#',time_str('Pretty')),
	dummy('steer_motor_target_data',(1,20)),
	dummy('metadata',(1,6,14,26)),
	dummy('ZED_data_pool2',(1,12,94,168)),

	conv("conv1",'ZED_data_pool2',96,1,11,3,0,"gaussian",std='0.00001'),
	relu("conv1"),
	pool("conv1","MAX",3,2,0),
	drop('conv1_pool',0.0),

	concat('conv1_metadata_concat',["conv1_pool","metadata"],1),

	conv("conv2",'conv1_metadata_concat',256,2,3,2,0,"gaussian",std='0.1'),
	relu("conv2"),
	pool("conv2","MAX",3,2,0),
	drop('conv2_pool',0.0),
	ip("ip1","conv2_pool",512,"xavier",std=0),
	relu('ip1'),
	drop('ip1',0.0),
	ip("ip2","ip1",20,"xavier",std=0),
	euclidean("euclidean","steer_motor_target_data","ip2")
]
#
##############################################################################
##############################################################################
##############################################################################







if TRAIN:
	TEST = False
else:
	TEST = True

unix(d2s('mkdir -p',opjD(fname(model_path))))

USE_GPU = True
if USE_GPU:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

"""
for t in train_val_lst:
	print t
list_of_strings_to_txt_file(opj(model_path,'train_val.prototxt'),train_val_lst)
"""

if TEST:
	write_solver(model_path,base_lr=0.0,snapshot=100000000)
	test_solver_inputs_dic,test_keys = get_solver_inputs_dic_ks(test_runs_folder)
	median_errors = []
	if True:
		if len(gg(opjD(fname(model_path),'*.caffemodel'))) > 0:
			test_caffe_net = Caffe_Net(opj(model_path,'solver.prototxt'),version,weights_file_mode,weights_file_path,restore_solver=False)
			e = test(test_caffe_net,test_solver_inputs_dic,test_keys,version,model_path,test_time_limit)
			median_errors.append(e)
			figure('TEST ' + model_path + 'median errors',figsize=(2,2))
			plot(median_errors)
			plt.pause(0.0001)
		else:
			cprint("Can't test because no .caffemodel files",'red')
		print 'waiting . . .'
		time.sleep(60)

if TRAIN:
	write_solver(model_path,base_lr=base_lr,snapshot=snapshot)
	solver_inputs_dic,keys = get_solver_inputs_dic_ks(runs_folder,to_require=to_require,to_ignore=to_ignore)
	caffe_net = Caffe_Net(opj(model_path,'solver.prototxt'),version,weights_file_mode,weights_file_path,restore_solver=restore_solver)
	while True:
		try:
			train(caffe_net,solver_inputs_dic,keys,version,model_path,train_time_limit)
		except Exception as e:
			cprint("********** Exception ***********************",'red')
			print(e.message, e.args)
