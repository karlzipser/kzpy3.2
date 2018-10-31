from kzpy3.vis3 import *

h5py_runs_folder = opjk('Train_app/Train_SqueezeNet_flex/__local__/h5py')

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
	'FC0':'FC2',
	'FC1':'FC3',
	'FC2':'FC0',
	'FC3':'FC1',
}

Flex_location_dic = {
	'FL0':0,
	'FL1':0,
	'FL2':1,
	'FL3':1,
	'FR0':4,
	'FR1':4,
	'FR2':5,
	'FR3':5,
	'FC0':3,
	'FC1':3,
	'FC2':2,
	'FC3':2,		
}

Flex_channel_dic = {
	'FL0':0,
	'FL1':1,
	'FL2':0,
	'FL3':1,
	'FR0':0,
	'FR1':1,
	'FR2':0,
	'FR3':1,
	'FC0':0,
	'FC1':1,
	'FC2':0,
	'FC3':1,		
}

num_backward_timesteps,num_forward_timesteps,num_flex_locations = 18,18,6

def get_flex_data(h5py_runs_folder):
	F = {}
	for t in topics:
		F[t] = na([])

	runs = sggo(h5py_runs_folder,'*')

	for r in runs:
		cs(r)
		L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
		for t in topics:
			lt = L[t][:]
			#print(len(lt))
			F[t] = np.concatenate((F[t],L[t][:]),axis=0)
		L.close()

	F['motor_categorized'] = F['motor'].copy()
	F['motor_categorized'][F['motor']<45] = 1
	F['motor_categorized'][F['motor']>=45] = 0
	F['motor_neutral_span'] = 0*F['motor']
	for i in range(len(F['motor'])-num_backward_timesteps):
		if np.sum(F['motor_categorized'][i:i+num_backward_timesteps]) == 0:
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
			continue
			F['motor scaled'] = F['motor'].copy()
			F['motor scaled'][0] = 0
			F['motor scaled'][1] = 99
			F['motor scaled'] = z2o(F['motor scaled'])
		elif t == 'steer':
			continue
			F['steer scaled'] = F['steer'].copy()
			F['steer scaled'][0] = 0
			F['steer scaled'][1] = 99
			F['steer scaled'] = z2o(F['steer scaled'])
		elif t == 'gyro_heading_x':
			continue
			F['gyro_heading_x scaled'] = F['gyro_heading_x'].copy()

	return F



def get_flex_segs(F,flip=False):
	
	#index += 1
	index = np.random.randint(num_backward_timesteps,len(F['steer'])-num_forward_timesteps)
	#print index
	Flex_segs = {}

	flexed = False

	for topic in topics:
		if topic[0] == 'F':
			if flip:
				the_topic = Flex_flip_dic[topic]
			else:
				the_topic = topic
		elif topic in ['steer','motor']:
			the_topic = topic
		Flex_segs[the_topic] = F[the_topic][index-num_backward_timesteps:index+num_forward_timesteps]

	if flip:
		Flex_segs['steer'] = 99-Flex_segs['steer']

	return Flex_segs


def make_flex_image(Fs,noise=False):
	if noise == False:
		img = zeros((num_backward_timesteps,3*num_flex_locations,3))
	else:
		img = noise * np.random.randn(num_backward_timesteps,3*num_flex_locations,3)
	for f in Fs.keys():
		if f[0] == 'F':
			x = Flex_location_dic[f]
			c = Flex_channel_dic[f]
		#for t in range(num_backward_timesteps):
		for i in range(3):
			img[:,3*x+i,c] += Fs[f][:num_backward_timesteps]#[t]

	return img


def get_input_target_data():
	
	return D


def test(flip=False,proportion_flex_run=1.0):
	clf()
	N=get_flex_segs(F,flip,proportion_flex_run)
	print N.keys()
	for t in N.keys():
		if 'F' == t[0]:
			plot(N[t])
		elif t == 'motor scaled':
			plot(N[t],'b.-')
		elif t == 'steer scaled':
			plot(N[t],'r.-')
	xylim(0,num_backward_timesteps+num_forward_timesteps,0,1)


#import kzpy3.Data_app.collect_flex_data2 as fx
if False:
	F = get_flex_data(h5py_runs_folder)

	Fs = get_flex_segs(F,flip=False)
	dimg = zeros((num_backward_timesteps+1,3*num_flex_locations,3))
	dimg[num_backward_timesteps,:,:]=2000
	dimg[num_backward_timesteps,0,:]=-2000
	m = make_flex_image(Fs)
	index = 0
	indicies = []
	for i in range(18):
		indicies.append(index)
		index += random.choice([1,2])
	assert len(indicies) == 18
	assert max(indicies) < 36
	n=m[indicies,:,:]

	if graphics:
		dimg[:num_backward_timesteps,:,:] = m
		mi(z2o(dimg),'img')
		figure('motor');clf()
		plot(49+0*Fs['steer'][num_backward_timesteps:],'k-')
		plot(Fs['motor'][num_backward_timesteps:],'b.-')
		plot(Fs['steer'][num_backward_timesteps:],'r.-')
		ylim(0,99)
		spause()

# so(opjk('Train_app/Train_SqueezeNet_40_flex/__local__/Flex_data'),F)

#EOF