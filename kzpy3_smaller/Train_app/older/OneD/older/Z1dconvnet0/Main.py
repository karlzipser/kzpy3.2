###start
from kzpy3.vis3 import *
import torch
from kzpy3.utils3 import *
import kzpy3.Menu_app.menu
import kzpy3.Train_app.Train_Z1dconvnet0.default_values as default_values
import kzpy3.Train_app.Train_Z1dconvnet0.Network_Module as Network_Module
exec(identify_file_str)

#rsync -ravLp --exclude='flip*' --exclude='original*' /media/karlzipser/rosbags/flex_sensors_Aug2018/* /media/karlzipser/rosbags/flex_sensors_Aug2018_bkp/
"""
P = default_values.P
menu_path = P['The menu path.']
unix('mkdir -p '+menu_path)
unix(d2s('rm',opj(menu_path,'ready')))
kzpy3.Menu_app.menu.save_topics(P,P['The menu path.'])
unix(d2s('touch',opj(menu_path,'ready')))
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,P]).start()
"""

###stop
topics = [
 #u'acc_x',
 #u'acc_y',
 #u'acc_z',
 u'encoder',
 #u'gyro_x',
 #u'gyro_y',
 #u'gyro_z',
 u'cmd_steer',
 u'cmd_motor',
 u'drive_mode',
 u'human_agent',
 #u'motor',
 #u'steer',
 u'xfc0',
 u'xfl0',
 u'xfl1',
 u'xfr0',
 u'xfr1',
]

num_topics = len(topics)
num_minibatches = 2
num_input_timesteps = 60

Network = Network_Module.Pytorch_Network(weights_file_path=most_recent_file_in_folder(opjD('flex_net_0/weights/weights'),['sfn'],[]),network_output_folder=opjD('flex_net_0/weights'),safe_file_name="sfn")


list_of_h5py_folders = sggo('/media/karlzipser/rosbags/flex_sensors_Aug2018_bkp/*')#h5py/*')
M = {}
for t in topics:
	M[t] = na([])
M_temp = {}
for t in topics+['motor','steer']:
	M[t] = na([])
for f in list_of_h5py_folders:
	pd2s(f)
	runs = sggo(f,'*')
	for r in runs:
		pd2s('\t',r)
		try:
			L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
			print L['motor']
			for t in M.keys():
				M_temp[t] = L[t][:] #if topic not in file, this will raise exception, avoiding adding partial data to M.
			for t in M.keys():
				print('adding '+t)
				M[t] = np.concatenate((M[t],M_temp[t]),axis=None)
				#figure(d2s(t,':',fname(r)));clf();plot(M[t])
			#raw_enter()
			#CA()
		except:
			exec(EXCEPT_STR)
		try:
			L.close()
		except:
			exec(EXCEPT_STR)
	#for t in M.keys():
	#	figure(d2s(t,': all runs'));clf();plot(M[t])
	#raw_enter()
	#CA()

L={}
for t in M.keys():
	L[t] = zscore(M[t][:])
#for t in M.keys():
#	figure(d2s(t,': all runs'));clf();plot(L[t])
#raw_enter()
#CA()


the_input = torch.FloatTensor(num_minibatches,num_topics,num_input_timesteps).zero_().cuda()
the_target = torch.FloatTensor(num_minibatches,20,1).zero_().cuda()

target_index_range = na(range(0,30,3))
timeindex_offset = 0
display_timer = Timer(4)
display_timer2 = Timer(1)
display_timer3 = Timer(10)
rate_counter = Timer(10)

def get_time_index(Time_indicies):
	
	return i

find_timer = Timer(1/10000.0)
epoch_num = 0
while True:
	try:
		epoch_num += 1
		CS_(d2s('starting epoch',epoch_num))
		Time_indicies = range(timeindex_offset+num_input_timesteps,len(L['encoder'][:])-num_input_timesteps)
		while len(Time_indicies) > 280000:#num_minibatches:
			batch = 0
			while batch < num_minibatches:
				i = np.random.randint(len(Time_indicies))
				time_index = Time_indicies[i]

				target_motor = list(L['motor'][time_index+target_index_range])
				target_steer = list(L['steer'][time_index+target_index_range])
				if (( max(abs(target_steer)) > 0.75) or (max(abs(target_motor)) > 0.75)) or (np.random.randint(10)<1):
					assert(len(target_motor)==10)
					assert(len(target_steer)==10)
					the_target[batch,0:20,0]=torch.from_numpy(na(target_steer+target_motor))
					_topic_ctr = 0
					for t in topics:
						the_input[batch,_topic_ctr,:] = torch.from_numpy(L[t][(-num_input_timesteps+time_index):time_index])
						_topic_ctr += 1
					del Time_indicies[i]
					batch += 1
				find_timer.reset()
			freq = rate_counter.freq(do_print=False)
			if freq != False:
				pd2s(num_minibatches*freq,'Hz')
			#print type(the_input),type(the_target),type(Network['forward'])

			Network['forward'](the_input,the_target)

			Network['backward']()

			Network['save net']()

			if display_timer.check():
				print len(Time_indicies)
				figure(1);clf();ylim(-6,6);plot(target_steer,'r:');plot(target_motor,'b:');
				the_output = Network['net'].C['output'][0].data.cpu().numpy()
				output_steer = the_output[0:10]
				output_motor = the_output[10:20]
				plot(output_steer,'r.-')
				plot(output_motor,'b.-')
				spause()
				display_timer.reset()
				#if display_timer3.check():
				for l in ['input','conv1/relu','conv2/relu','conv3']:#,'ip1']:
					n = Network['net'].C[l][0].data.cpu().numpy()
					mi(z2o(n),l)
				plt.pause(0.1)
				spause()
				display_timer3.reset()

	except KeyboardInterrupt:
		#P['ABORT'] = True
		exec(EXCEPT_STR)
		break
	except Exception as e:
		pd2s("Main.py Exception",e)
		exec(EXCEPT_STR)

CS_('done.')

def get_print_exec_str(List_of_names):
	s = """ \b"pd2s("""
	for l in List_of_names:
		s += d2n("'",l," = ',",l,',')
	s += """ )" """
	return s
#EOF