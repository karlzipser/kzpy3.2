from kzpy3.vis3 import *



################################################################################
#
Arguments['path'] = opjD('Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop')

data_path = Arguments['path']
behavioral_modes = ['left','right','direct','stop']
steers = ['low_steer','high_steer','reverse']

Data_moments_dic = lo(opj(data_path,'data_moments_dic.pkl'))

all_moments = []
for u in ['train','val']:
    for v in steers:
        if v in Data_moments_dic[u]:
            for i in rlen(Data_moments_dic[u][v]):
                Data_moments_dic[u][v][i]['steer_type'] = v
            all_moments += Data_moments_dic[u][v]

Organized_moments = {}

for a in all_moments:

    r = a['run_name']

    if r not in Organized_moments:
        Organized_moments[r] = {}
        for b in behavioral_modes:
            Organized_moments[r][b] = {}
            for s in steers:
                Organized_moments[r][b][s] = []

    b = a['behavioral_mode']
    if b == 'center':
        b = 'direct'
        a['behavioral_mode'] = b

    if b not in behavioral_modes:
        cr(b,'not in',behavioral_modes)

    Organized_moments[r][b][a['steer_type']].append(a)
#
######################
#

S = {}
Ctrs = {}         
C = {'left':'r.','right':'g.','direct':'b.','stop':'c.','center':'y.','reverse':'k.'}
CA()

for r in Organized_moments.keys():
    ectr = 0
    ctr = 0

    L = h5r(opj(data_path,'h5py',r,'left_timestamp_metadata_right_ts.h5py'))
    
    S[r] = {}
    for b in ['left','right','direct']:
        S[r][b] = {}
        for s in steers:
            o = Organized_moments[r][b][s]

            S[r][b][s] = {}
            for m in o:

                i = m['left_ts_index'][1]

                if np.abs(m['motor']-49) < 2 and np.abs(m['steer']-49) < 2 and m['behavioral_mode'] in ['left','right','center']:
                    #cr('.')
                    ctr+=1
                    continue
                if L['encoder'][i] < 0.1:
                    #cr('+')
                    continue
                    ectr+=1
                try:
                    if np.std(L['steer'][i-30:i+30]) < 1.0:
                        #cr('x')
                        ectr+=1
                        continue
                        
                except:
                    continue

                S[r][b][s][i] = m
                ctr+=1

            _,indexed_moments = get_key_sorted_elements_of_dic(S[r][b][s])
            S[r][b][s] = indexed_moments
            if True:
                figure(1)
                ii=[]
                els=S[r][b][s]
                for e in els:
                    ii.append(e['left_ts_index'][1])
                cg(r,b,s,len(ii))   
                if b == 'direct' and s == 'reverse':
                    c = 'k.'
                else:
                    c = C[b]
                plot(ii,c); spause()
                
                #raw_enter()
    Ctrs[r] = ctr        
    cy(r,ectr,ctr,int(ectr*100.0/(ctr*1.0)),'%')
    L.close()
    #raw_enter()


#
######################
#




Randomized_moments = {}
Indicies = {}
Counts = {}

for r in S.keys():
    Indicies[r] = []
    Counts[r] = {}
    cg('Randomized_moments for',r)
    Randomized_moments[r] = []

    n_desired_moments = int(Ctrs[r]*0.1)

    for b in ['left','right','direct']:
        for s in ['low_steer','high_steer','reverse']:
            random.shuffle(S[r][b][s])

    while len(Randomized_moments[r]) < n_desired_moments:
        len_prev = len(Randomized_moments[r])
        for b in ['left','right','direct']:
            for s in ['low_steer','high_steer','reverse']:
                if len(S[r][b][s]) > 0:
                    Randomized_moments[r].append(S[r][b][s].pop())
        if len_prev == len(Randomized_moments[r]):
            cr("*** waring no progress beyond",len_prev,"for",r)


    for b in ['left','right','direct']:
        Counts[r][b] = {}
        for s in ['low_steer','high_steer','reverse']:
            Counts[r][b][s] = 0
    for m in Randomized_moments[r]:
        Counts[r][m['behavioral_mode']][m['steer_type']] += 1
        Indicies[r].append(m['left_ts_index'][1])

#
######################
#


O = h5r(opj(data_path,'h5py',r,'original_timestamp_data.h5py'))
L = h5r(opj(data_path,'h5py',r,'left_timestamp_metadata_right_ts.h5py'))
F = h5r(opj(data_path,'h5py',r,'flip_images.h5py'))

Behavioral_mode_code = {
	'left':110,
	'right':111,
	'direct':112,
}

topics = [
	'encoder_meo',
	'name',
	'behavioral_mode',
	'behavioral_mode_code',
	'gyro_heading_x',
	'FLIP',
	'encoder_past',
	'right',
	'projections',
	'motor',
	'steer',
	'left',
]

H = {}
for t in topics:
	H[t] = []

for i in range(100):
	cr('i =',i)

	H['name'].append(r)

	m = Randomized_moments[r][i]

	l = m['left_ts_index'][1]
	rr = m['right_ts_index'][1]

	behavioral_mode = m['behavioral_mode']
	heading_x = L['gyro_heading_x'][l:l+90]
	steer = L['steer'][l:l+90].astype(np.uint8)
	motor = L['motor'][l:l+90].astype(np.uint8)
	flip = np.random.choice([0,1])

	H['FLIP'].append(flip)

	if flip:
		steer = 99 - steer
		heading_x *= -1.0
		if behavioral_mode == 'left':
			behavioral_mode = 'right'
		elif behavioral_mode == 'right':
			behavioral_mode = 'left'
		IL = F['left_image_flip']['vals']
		IR = F['right_image_flip']['vals']
		H['left'].append([IR[l],IR[l+1]])
		H['right'].append([IL[l],IL[rr+1]])
	else:
		IL = O['left_image']['vals']
		IR = O['right_image']['vals']
		H['left'].append([IL[l],IL[l+1]])
		H['right'].append([IR[rr],IR[rr+1]])
	steer[steer > 99] = 99
	steer[steer < 0] = 0
	motor[motor > 99] = 99
	motor[motor < 0] = 0

	H['behavioral_mode'].append(behavioral_mode)
	H['behavioral_mode_code'].append(Behavioral_mode_code[H['behavioral_mode']])
	H['encoder_meo'].append(L['encoder_meo'][l:l+90])
	H['gyro_heading_x'].append(heading_x)
	H['steer'].append(steer)
	H['motor'].append(motor)
	H['encoder_past'].append(L['encoder_meo'][l-70:l-1])

	mi( [ H['right'][-1][0], H['left'][-1][0], H['right'][-1][1],H['left'][-1][1] ],0)
	plt.title(d2s(H['name'][-1],H['behavioral_mode'][-1],H['FLIP'][-1]))
	figure(2);clf();plot(H['steer'][-1]);plot(H['motor'][-1]);plot(H['encoder_meo'][-1]*10);plot(H['gyro_heading_x'][-1]-H['gyro_heading_x'][-1][0]);plot(H['encoder_past'][-1]*10);plot(H['steer'][-1]);

	spause();raw_enter()







#
################################################################################







#EOF