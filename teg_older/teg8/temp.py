from kzpy3.caf6.cafutils import *
from kzpy3.caf6.protos import *

def print_solver(solver):
	print("")
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	print("")
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		if 'split' not in l[0]:
			print(l)

def setup_solver(solver_file_path):
	solver = caffe.SGDSolver(solver_file_path)
	print_solver(solver)
	return solver

##############################################################################
#
model_path = opjh("kzpy3/caf7/z3_color")
gpu = None
restore_solver = False
base_lr = 0.05
snapshot = 100000
#ignore = [reject_run,left,out1_in2,Smyth,racing] # runs with these labels are ignored
require_one = [] # at least one of this type of run lable is required
use_states = [1]
weights_file_mode = 'most recent' # 'this one' #None #'most recent' #None #'most recent'
weights_file_path =  opjD(fname(model_path)) #opjD('z2_color_trained_12_15_2016') #opjD('z2_color_long_train_21_Jan2017') #None #opjh('kzpy3/caf6/z2_color/z2_color.caffemodel') #None #'/home/karlzipser/Desktop/z2_color' # None #opjD('z2_color')
#
##############################################################################
#
"""
layer {
  name: "left_pool_pool_scale"
  type: "Scale"
  bottom: "left_pool_pool"
  top: "left_pool_pool_scale"
  param {
    lr_mult: 0
    decay_mult: 0
  }
  param {
    lr_mult: 0
    decay_mult: 0
  }
  scale_param {
    filler {
      value: 0.003921    }
    bias_term: true
    bias_filler {
      value: -0.5
    }
  }
}
"""

"""
layer {
  name: "left_pool_pool_scale"
  type: "Scale"
  bottom: "left_pool_pool"
  top: "left_pool_pool_scale"
  param {
    lr_mult: 0
    decay_mult: 0
  }
  param {
    lr_mult: 0
    decay_mult: 0
  }
  scale_param {
    filler {
      value: 0.003921    }
    bias_term: true
    bias_filler {
      value: -0.5
    }
  }
}
"""
train_val_lst = [

	d2s('#',model_path),
	d2s('#',time_str('Pretty')),

	dummy('left_t_0',(1,3,376,672)),
	pool("left_t0","AVE",1,2,0),
	pool("left_t0_pool","AVE",1,2,0),

	dummy('left_t_neg1_pool_pool',(1,3,94,168)),
	dummy('left_t_neg2_pool_pool',(1,3,94,168)),

	dummy('right',(1,9,376,672)),
	pool("right","AVE",3,2,0),
	pool("right_pool","AVE",3,2,0),
	#dummy('left_pool2',(1,12,94,168)),
	#dummy('right_pool2',(1,12,94,168)),

	dummy('steer_motor_target_data',(1,60)),
	#dummy('motor_target_data',(1,30)),
	dummy('metadata',(1,6,11,20)),
	dummy('past_steer',(1,30,11,20)),

	dummy('past_motor',(1,30,11,20)),
	dummy('xy_gradients',(1,2,11,20)),

	conv("conv1_left",'left_pool_pool',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv1_left"),
	pool("conv1_left","MAX",3,2,0),


	conv("conv1_right",'right_pool_pool',48,1,3,2,0,"gaussian",std='0.00001'),
	relu("conv1_right"),
	pool("conv1_right","MAX",3,2,0),

	concat('conv1_concat',["conv1_left","conv1_right"],1),
	concat('conv1_pool_concat',["conv1_left_pool","conv1_right_pool"],1),

	conv("conv2a_bi",'conv1_concat',96,1,3,2,0,"gaussian",std='0.1'),
	relu("conv2a_bi"),
	pool("conv2a_bi","MAX",3,2,0),

	conv("conv2b_bi",'conv1_pool_concat',96,1,3,2,0,"gaussian",std='0.1'),
	relu("conv2b_bi"),




	drop('past_steer',0.5),
	drop('past_motor',0.5),

	concat('conv2_concat',["conv2a_bi_pool","conv2b_bi","metadata","past_steer","past_motor","xy_gradients"],1),

	conv("conv2_1x1",'conv2_concat',96,1,1,1,0,"gaussian",std='0.1'),
	relu("conv2_1x1"),
	conv("conv2_3x3",'conv2_concat',96,1,3,1,[1,1],"gaussian",std='0.1'),
	relu("conv2_3x3"),

	concat('conv2_final_concat',["conv2_1x1","conv2_3x3"],1),

	conv("conv3",'conv2_final_concat',96,1,3,1,[1,1],"gaussian",std='0.1'),
	relu("conv3"),
	pool("conv3","MAX",3,2,0),

	ip("ip1","conv3_pool",512,"xavier",std=0),
	relu('ip1'),
	drop('ip1',0.0),
	ip("ip2","ip1",60,"xavier",std=0),
	euclidean("euclidean","steer_motor_target_data","ip2")
	
]
#
##############################################################################
##############################################################################
##############################################################################

unix(d2s('mkdir -p',opjD(fname(model_path))))

if gpu != None:
	caffe.set_device(gpu)
	caffe.set_mode_gpu()

for t in train_val_lst:
	print t
list_of_strings_to_txt_file(opj(model_path,'train_val.prototxt'),train_val_lst)

write_solver(model_path,base_lr=base_lr,snapshot=snapshot)

setup_solver(opj(model_path,'solver.prototxt'))

