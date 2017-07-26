
REPO = 'kzpy3'
CAF = 'caf8'
MODEL = 'z2_color_aruco'

from kzpy3.utils2 import *
import kzpy3.caf8.protos as protos

##############################################################################
#
model_path = opjh(REPO,CAF,MODEL)

batch_size = 1

loss_weight = 1.0

train_val_lst = [d2s('#',model_path),d2s('#',time_str('Pretty'))]

train_val_lst += [
	d2s('#',model_path),
	d2s('#',time_str('Pretty')),

	protos.dummy('other_car_inverse_distances',(batch_size,11)),
	protos.dummy('marker_inverse_distances',(batch_size,11)),
	protos.dummy('potential_values',(batch_size,11)),
	protos.dummy('clock_potential_values',(batch_size,11)),
	protos.dummy('steer',(batch_size,1)),
	protos.dummy('motor',(batch_size,1)),
	protos.dummy('velocity',(batch_size,1)),

	protos.dummy('metadata',(batch_size,6,14,26)),
	protos.dummy('ZED_data_pool2',(batch_size,12,94,168)),
	protos.scale('ZED_data_pool2_scale','ZED_data_pool2',0.003921,-0.5),

	protos.conv("conv1",'ZED_data_pool2_scale',96,1,11,3,0,"gaussian",std='0.00001'),
	protos.relu("conv1"),
	protos.pool("conv1","MAX",3,2,0),

	protos.concat('conv1_metadata_concat',["conv1_pool","metadata"],1), 

	protos.conv("conv2",'conv1_metadata_concat',256,2,3,2,0,"gaussian",std='0.1'),
	protos.relu("conv2"),
	protos.pool("conv2","MAX",3,2,0),
	protos.drop('conv2_pool',0.0),
	protos.ip("ip1","conv2_pool",512,"xavier",std=0),
	protos.relu('ip1'),






	protos.ip("ip_other_car_inverse_distances","ip1",11,"xavier",std=0),
	protos.euclidean("euclidean_other_car_inverse_distances","other_car_inverse_distances","ip_other_car_inverse_distances"),

	protos.ip("ip_marker_inverse_distances","ip1",11,"xavier",std=0),
	protos.euclidean("euclidean_marker_inverse_distances","marker_inverse_distances","ip_marker_inverse_distances",loss_weight),

	protos.ip("ip_potential_values","ip1",11,"xavier",std=0),
	protos.euclidean("euclidean_potential_values","potential_values","ip_potential_values",loss_weight),

	protos.ip("ip_clock_potential_values","ip1",11,"xavier",std=0),
	protos.euclidean("euclidean_clock_potential_values","clock_potential_values","ip_clock_potential_values",loss_weight),


	protos.ip("ip_velocity","ip1",1,"xavier",std=0),
	protos.euclidean("euclidean_velocity","velocity","ip_velocity",loss_weight),


	protos.concat('ip_concat',["ip_other_car_inverse_distances","ip_marker_inverse_distances",
		"ip_potential_values","ip_clock_potential_values","ip_velocity"],1),

	protos.ip("ip2__steer","ip_concat",20,"xavier",std=0),
	protos.relu('ip2__steer'),
	protos.ip("ip3_steer","ip2__steer",1,"xavier",std=0),

	protos.ip("ip2__motor","ip_concat",20,"xavier",std=0),
	protos.relu('ip2__motor'),
	protos.ip("ip3_motor","ip2__motor",1,"xavier",std=0),


	protos.euclidean("euclidean_steer","steer","ip3_steer",loss_weight),
	protos.euclidean("euclidean_motor","motor","ip3_motor",loss_weight),
]


solver_lst =  [
	d2s('#',model_path),
	d2s('#',time_str('Pretty')),
	protos.solver_proto(
	model_path=model_path,
	test_iter=1,
	test_interval=1000000,
	test_initialization='false',
	base_lr = 0.0001,
	momentum=0.0001,
	weight_decay='0.000005',
	lr_policy="inv",
	gamma=0.0001,
	power=0.75,
	display=20000,
	max_iter=10000000,
	snapshot=50000
	)]
#
##############################################################################


unix(d2s('mkdir -p',opjD(fname(model_path))))

for t in train_val_lst:
	print t
print('')
for t in solver_lst:
	print t

list_of_strings_to_txt_file(opj(model_path,'train_val.prototxt'),train_val_lst)
solver_path = opj(model_path,'solver.prototxt')
list_of_strings_to_txt_file(solver_path,solver_lst)

solver = protos.setup_solver(solver_path)



def put_data_into_model(data,solver,b=0):
	############## load data into solver #####################
	#
	ctr = 0
	for c in range(3):
		for camera in ['left','right']:
			for t in range(2):
				solver.net.blobs['ZED_data_pool2'].data[b,ctr,:,:] = data[camera][t][:,:,c]
				ctr += 1

	Racing = 0
	Desired_Direction = 0
	Follow = 0
	Direct = 0
	Play = 0
	Furtive = 0
	if data['behavioral_mode'] == 'Follow_Arena_Potential_Field':
		Follow = 1.0
	if data['behavioral_mode'] == 'Direct_Arena_Potential_Field':
		Direct = 1.0
	if data['behavioral_mode'] == 'Play_Arena_Potential_Field':
		Play = 1.0
	if data['behavioral_mode'] == 'Furtive_Arena_Potential_Field':
		Furtive = 1.0


	solver.net.blobs['metadata'].data[b,0,:,:] = Racing
	solver.net.blobs['metadata'].data[b,1,:,:] = data['desired_direction']
	solver.net.blobs['metadata'].data[b,2,:,:] = Follow
	solver.net.blobs['metadata'].data[b,3,:,:] = Direct
	solver.net.blobs['metadata'].data[b,4,:,:] = Play
	solver.net.blobs['metadata'].data[b,5,:,:] = Furtive

	if len(data['other_car_inverse_distances']) > 0:
		solver.net.blobs['other_car_inverse_distances'].data[b,:] = data['other_car_inverse_distances']
	else:
		solver.net.blobs['other_car_inverse_distances'].data[b,:] *= 0
	solver.net.blobs['marker_inverse_distances'].data[b,:] = data['marker_inverse_distances']
	solver.net.blobs['potential_values'].data[b,:] = data['potential_values']
	solver.net.blobs['clock_potential_values'].data[b,:] = data['clock_potential_values']
	solver.net.blobs['velocity'].data[b,:] = data['velocity']

	solver.net.blobs['steer'].data[b,:] = data['steer']/99.
	solver.net.blobs['motor'].data[b,:] = data['motor'][-1]/99.
	#
	##########################################################










