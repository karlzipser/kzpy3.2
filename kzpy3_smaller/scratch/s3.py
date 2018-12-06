from kzpy3.vis3 import *
"""
if False:

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


###start




if False:
	buttons = {
		1:'sidewalk',
		2:'grass',
		3:'driveway',
		4:'street'
		}
	b = 1
	b_prev = 0
	while True:#b != -1:
		s = input("button: ")

		extra = ''
		if s == 1:
			extra = 'selected '
			say(extra+buttons[b_prev],rate=300)
		else:
			say(buttons[b],rate=300)
		b_prev = b
		b = b+1
		if b > 4:
			b = 1
		if b == -1:
			break
"""

if False:
	figure(1)
	L=h5r('/Volumes/transfer/flex_sensors_Aug2018/h5py/Mr_Blue_Back_23Aug18_18h24m30s/left_timestamp_metadata_right_ts.h5py')

	for i in range(3000,len(L['gyro_heading_x'][:]),10):
		clf()
		ylim(-50,100)
		plot(L['gyro_heading_x'][i:i+90]-L['gyro_heading_x'][i+45],'b.')
		plot(L['cmd_steer'][i:i+90],'r.')
		plot(L['steer'][i:i+90],'go')
		plot([0,90],[49,49],'k')
		plot([0,90],[0,0],'k')
		plt.pause(0.1)
 
if True:
	figure(1);cl()
	L=h5r('/Volumes/transfer/flex_sensors_Aug2018/h5py/Mr_Blue_Back_23Aug18_18h24m30s/left_timestamp_metadata_right_ts.h5py')

	for i in range(3000,len(L['gyro_heading_x'][:]),10):
		#clf()
		ylim(-50,100)
		plot(L['gyro_heading_x'][i:i+90]-L['gyro_heading_x'][i+45],'b.')
		plot(L['cmd_steer'][i:i+90],'r.')
		plot(L['steer'][i:i+90],'go')
		plot([0,90],[49,49],'k')
		plot([0,90],[0,0],'k')
		plt.pause(0.1)


plot(L['GPS_latitudeDegrees'],L['GPS_longitudeDegrees'],'.')
###stop
#EOF
# https://github.com/vgm64/gmplot
from gmplot import gmplot

# Place map
gmap = gmplot.GoogleMapPlotter(latitudes[10000], longitudes[10000], 13)
"""
# Polygon
golden_gate_park_lats, golden_gate_park_lons = zip(*[
    (37.771269, -122.511015),
    (37.773495, -122.464830),
    (37.774797, -122.454538),
    (37.771988, -122.454018),
    (37.773646, -122.440979),
    (37.772742, -122.440797),
    (37.771096, -122.453889),
    (37.768669, -122.453518),
    (37.766227, -122.460213),
    (37.764028, -122.510347),
    (37.771269, -122.511015)
    ])
gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)

# Scatter points
top_attraction_lats, top_attraction_lons = zip(*[
    (37.769901, -122.498331),
    (37.768645, -122.475328),
    (37.771478, -122.468677),
    (37.769867, -122.466102),
    (37.767187, -122.467496),
    (37.770104, -122.470436)
    ])
"""
grange = range(60000,70000,5)
gmap.scatter(L['GPS_latitudeDegrees'][grange],L['GPS_longitudeDegrees'][grange], '#3B0B39', size=1, marker=False)
gmap.draw(opjD("my_map0.html"))



