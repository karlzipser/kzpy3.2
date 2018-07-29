from kzpy3.vis2 import *


D1 = {'file':opjh('Desktop2','Mr_Black_25Jul18_14h29m56s_local_lrc/left_timestamp_metadata_right_ts.h5py'),
	'correcctions':[
		{'topic':'drive_mode','start':0,'stop':10000,'value':0,'type':'int','op':'mult'},
		{'topic':'drive_mode','start':15900,'stop':17500,'value':0,'type':'int','op':'mult'},
		{'topic':'drive_mode','start':20600,'stop':20800,'value':0,'type':'int','op':'mult'},
		{'topic':'drive_mode','start':22500,'stop':23000,'value':0,'type':'int','op':'mult'},
		{'topic':'motor','start':17500,'stop':22100,'value':-5,'type':'int','op':'add'},
		],
	'corrected_data':{}
	}

D2 = {'file':opjh('Desktop2','direct_home_LCR_16Jun18_20h22m37s_Mr_Silver_Green/left_timestamp_metadata_right_ts.h5py'),
	'correcctions':[
		{'topic':'state','start':10450,'stop':10725,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':14750,'stop':15000,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':17100,'stop':18350,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':21200,'stop':21400,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':12800,'stop':13100,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':31300,'stop':31800,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':33000,'stop':34400,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':34800,'stop':35300,'value':4,'type':'int','op':'eql'},
		{'topic':'motor','start':10450,'stop':32550,'value':8,'type':'int','op':'add'},
		{'topic':'motor','start':0,'stop':10450,'value':-2,'type':'int','op':'add'},
		{'topic':'steer','start':26000,'stop':31300,'value':13,'type':'int','op':'add'},
		],
	'corrected_data':{}
	}

D3 = {'file':opjh('Desktop2','direct_home_LCR_07Jun18_16h47m05s_Mr_Green_Silver/left_timestamp_metadata_right_ts.h5py'),
	'correcctions':[
		{'topic':'state','start':21500,'stop':21900,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':12700,'stop':12900,'value':4,'type':'int','op':'eql'},
		{'topic':'state','start':16500,'stop':17000,'value':4,'type':'int','op':'eql'},
		{'topic':'motor','start':10900,'stop':16700,'value':11,'type':'int','op':'add'},
		{'topic':'steer','start':10850,'stop':16720,'value':-8,'type':'int','op':'add'},
		],
	'corrected_data':{}
	}

D = D1

try:
  L
except NameError:
  pd2s('Loading',D['file'])
  #L = h5r(D['file'])
  L= h5py.File(D['file'], 'r+')
else:
  pd2s(D['file'],"already loaded")

for C in D['correcctions']:
	topic = C['topic']
	if topic not in D['corrected_data']:
		print topic
		D['corrected_data'][topic] = L[topic][:]
	data = D['corrected_data'][topic]

	if C['op'] == 'add':
		data[C['start']:C['stop']] += C['value']
	elif C['op'] == 'mult':
		data[C['start']:C['stop']] *= C['value']
	elif C['op'] == 'eql':
		data[C['start']:C['stop']] = C['value']

	if C['type'] == 'int':
		data = data.astype(int)
	figure(topic)
	clf()
	plot(L[topic][:],'.')
	if 'drive_mode' in D['corrected_data']:
		for i in range(len(D['corrected_data']['drive_mode'])):
			if topic in ['steer','motor']:
				if D['corrected_data']['drive_mode'][i] == 0:
					data[i] = 49
	elif 'state' in D['corrected_data']:
		for i in range(len(D['corrected_data']['state'])):
			if topic in ['steer','motor']:
				if D['corrected_data']['state'][i] == 4:
					data[i] = 49
	plot(data,'.')

topics_dic = {}
for C in D['correcctions']:
	topics_dic[C['topic']] = True

for topic in topics_dic.keys():
	print topic
	data = L[topic]
	data[...] = D['corrected_data'][topic]
L.close()



#EOF


