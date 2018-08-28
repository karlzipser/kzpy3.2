	if False:
	#!/usr/bin/env python
	"""
	python kzpy3/Cars/car_16July2018/nodes/arduino_node.py
	"""
	from kzpy3.utils2 import *

	exec(identify_file_str)

	import default_values

	Parameters = default_values.Parameters

	import kzpy3.Menu_app.menu
	menu_path = opjh('kzpy3/Train_app/Train_Z1dconvnet0/__local__')
	unix('mkdir -p '+menu_path)
	unix(d2s('rm',opj(menu_path,'ready')))
	threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,Parameters]).start()



from kzpy3.vis2 import *
import torch

for a in Arguments.keys():
	P[a] = Arguments[a]
	spd2s(a,'=',P[a])


import kzpy3.Train_app.Train_Z1dconvnet0.Network_Module as Network_Module
exec(identify_file_str)

Network = Network_Module.Pytorch_Network()

display_timer = Timer(1)

# u'drive_mode',

topics = [
 u'acc_x',
 u'acc_y',
 u'acc_z',
 u'encoder',
 u'gyro_x',
 u'gyro_y',
 u'gyro_z',
 #u'motor',
 #u'steer',
 u'xfc0',
 u'xfl0',
 u'xfl1',
 u'xfr0',
 u'xfr1',
]

L = h5r(opjm('rosbags/flex_sensors_Aug2018/h5py/Mr_Blue_Back_24Aug18_18h49m37s/left_timestamp_metadata_right_ts.h5py'))
M = {}
for t in topics+['motor','steer']:
	M[t] = zscore(L[t][:])
L.close()
L = M
num_topics = len(topics)
num_minibatches = 2
num_input_timesteps = 60#150
the_input = torch.FloatTensor(num_minibatches,num_topics,num_input_timesteps).zero_().cuda()
the_target = torch.FloatTensor(num_minibatches,20,1).zero_().cuda()
#zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()

#motor = zeros((10,1))
#steer = zeros((10,1))
ctr = 0
target_index_range = na(range(0,30,3))
timeindex_offset = 0#10000]
rate_counter = Timer(5)

while True:
	if True:#try:
		for time_index in range(timeindex_offset+num_input_timesteps,len(L['acc_x'][:])-num_input_timesteps):
			#print time_index,len(L['acc_x'][:])-num_input_timesteps,len(L['acc_x'][:])
			
			
			for batch in range(num_minibatches):
				_topic_ctr = 0
				for t in topics:
					#print _topic_ctr
					the_input[batch,_topic_ctr,:] = torch.from_numpy(L[t][(-num_input_timesteps+time_index):time_index])
					_topic_ctr += 1
				motor = list(L['motor'][time_index+target_index_range])
				steer = list(L['steer'][time_index+target_index_range])
				assert(len(motor)==10)
				assert(len(steer)==10)
				
				#print(shape(np.concatenate([steer,motor])))
				the_target[batch,0:20,0]=torch.from_numpy(na(steer+motor))#np.concatenate([steer,motor]))
				#figure(2);plot(the_target)

			Network['forward'](the_input,the_target)
			Network['backward']()
			rate_counter.freq()
			ctr += 1
			if display_timer.check():
				#print ctr
				figure(1);clf();ylim(-6,6);plot(motor);plot(steer)#;spause();
				avg_pool = Network['net'].C['avg pool'][0].data.cpu().numpy()
				plot(avg_pool[0:10],'r.-')
				plot(avg_pool[10:20],'b.-')
				for l in ['input','conv1/relu','conv2/relu','conv3','avg pool']:
					n = Network['net'].C[l][0].data.cpu().numpy()
					#n[0,0],n[0,0] = 6,-6
					#print shape(n)
					mi(z2o(n),l)
				
				spause()
				#raw_enter()
				display_timer.reset()
	else:#except Exception as e:
		pd2s("Main.py Exception",e)


#EOF