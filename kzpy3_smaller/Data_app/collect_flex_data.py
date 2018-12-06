from kzpy3.vis3 import *

h5py_runs_folder = opjk('Train_app/Train_SqueezeNet_40_flex/__local__/h5py')

F = {}
topics = [
	'steer',
	'motor',
	'encoder_meo',
	'gyro_heading_x',
	'FL0',
	'FL1',
	'FL2',
	'FL3',
	'FR0',
	'FR1',
	'FR2',
	'FR3',
	'FC0',
	'FC1',
	'FC2',
	'FC3',
]

Flex_flip_dic = {
	'FL0':'FR0',
	'FL1':'FR1',
	'FL2':'FR2',
	'FL3':'FR3',
	'FR0':'FL0',
	'FR1':'FL1',
	'FR2':'FL2',
	'FR3':'FL3',
	'FC0':'FC3',
	'FC1':'FC2',
	'FC2':'FC1',
	'FC3':'FC0',
}

for t in topics:
	F[t] = na([])

runs = sggo(h5py_runs_folder,'*')


for r in runs:
	cs(r)
	L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
	for t in topics:
		lt = L[t][:]
		print(len(lt))
		F[t] = np.concatenate((F[t],L[t][:]),axis=0)
	L.close()

F['motor_categorized'] = F['motor'].copy()
F['motor_categorized'][F['motor']<45] = 1
F['motor_categorized'][F['motor']>=45] = 0
F['motor_neutral_span'] = 0*F['motor']
for i in range(len(F['motor'])-23):
	if np.sum(F['motor_categorized'][i:i+23]) == 0:
		F['motor_neutral_span'][i] = 1
F['motor_neutral_indicies'] = []
for i in range(len(F['motor_neutral_span'])):
	if F['motor_neutral_span'][i]:
		F['motor_neutral_indicies'].append(i)

for t in F.keys():
	if t[0]=='F':
		tsc = t+' scaled'
		F[tsc] = F[t].copy()
		F[tsc][F[tsc]>2000] = 2000
		F[tsc][F[tsc]<-2000] = -2000
		F[tsc][0] = -2000
		F[tsc][1] = 2000
		F[tsc] = z2o(F[tsc])
	elif t == 'motor':
		F['motor scaled'] = F['motor'].copy()
		F['motor scaled'][0] = 0
		F['motor scaled'][1] = 99
		F['motor scaled'] = z2o(F['motor scaled'])
	elif t == 'steer':
		F['steer scaled'] = F['steer'].copy()
		F['steer scaled'][0] = 0
		F['steer scaled'][1] = 99
		F['steer scaled'] = z2o(F['steer scaled'])
	elif t == 'gyro_heading_x':
		F['gyro_heading_x scaled'] = F['gyro_heading_x'].copy()



def get_Flex_segs(F,flip=False,proportion_flex_run=1.0):

	if np.random.random() > proportion_flex_run:
		index = random.choice(F['motor_neutral_indicies'])
	else:
		index = np.random.randint(0,len(F['steer scaled'])-23-90)
	Net_data = {}
	
	#print index
	Net_data['steer scaled'] = F['steer scaled'][index:index+23+90]
	Net_data['motor scaled'] = F['motor scaled'][index:index+23+90]
	F['gyro_heading_x']
	if flip:
		Net_data['steer scaled'] = 1.0-Net_data['steer scaled']

	flexed = False

	for topic in topics:
		if topic[0] == 'F':
			if flip:
				the_topic = Flex_flip_dic[topic]
			else:
				the_topic = topic
			Net_data[the_topic+' scaled'] = F[the_topic+' scaled'][index:index+23]
			q = np.abs(np.mean(Net_data[the_topic+' scaled'])-0.5)
			#print q
			if q > 0.1:
				flexed = True
	if not flexed:
		Net_data['steer scaled'] = 0*Net_data['steer scaled']+0.5
		Net_data['motor scaled'] = 0*Net_data['motor scaled']+0.5
	return Net_data



def test(flip=False,proportion_flex_run=1.0):
	clf()
	N=get_Flex_segs(F,flip,proportion_flex_run)
	print N.keys()
	for t in N.keys():
		if 'F' == t[0]:
			plot(N[t])
		elif t == 'motor scaled':
			plot(N[t],'b.-')
		elif t == 'steer scaled':
			plot(N[t],'r.-')
	xylim(0,23+90,0,1)


# so(opjk('Train_app/Train_SqueezeNet_40_flex/__local__/Flex_data'),F)

#EOF