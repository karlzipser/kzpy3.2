from kzpy3.vis3 import *

def get_validation_data(
    network_to_validate=None,
    num=None,
):
    weights_path = opjD('Networks',network_to_validate,'weights')

    ctime_sorted_weightfiles = sort_dir_by_ctime(weights_path)

    selected_weightfiles = []

    for i in range(0,len(ctime_sorted_weightfiles),len(ctime_sorted_weightfiles)/num):
        selected_weightfiles.append(ctime_sorted_weightfiles[i])
    if ctime_sorted_weightfiles[-1] not in selected_weightfiles:
        selected_weightfiles.append(ctime_sorted_weightfiles[-1])
    so(opjD('Networks',network_to_validate,'Val_lists'),
        {'ctime_sorted_weightfiles':ctime_sorted_weightfiles,
        'selected_weightfiles':selected_weightfiles})

    np.random.shuffle(selected_weightfiles)
    for w in selected_weightfiles:
        wait = True
        while wait:
            python_ps_ctr = 0
            processes = unix('ps -e')
            for p in processes:
                if ' python' in p:
                    python_ps_ctr += 1
            if python_ps_ctr < 10:
                wait = False
            else:
                clp(python_ps_ctr,'python_ps_ctr')
                time.sleep(10)

        sys_str =  d2s(
            "python kzpy3/Train_app/Sq120_ldr_output_4April2019/Main.py",
            "--VALIDATION_WEIGHTS_FILE_PATH",
            w,
            '&'
        )
        print sys_str
        os.system(sys_str)
        time.sleep(15)




def get_validation_curve(
    network_to_validate=None,
):
    Val_lists = lo(opjD('Networks',network_to_validate,'Val_lists'))
    ctime_sorted_weightfiles = Val_lists['ctime_sorted_weightfiles']
    selected_weightfiles = Val_lists['selected_weightfiles']
    validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))

    V = {}
    ctr = 0
    validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))

    for s in selected_weightfiles:
        V[fname(s)] = {'ctr':ctr,'lst':[]}
        ctr += 1

    for s in selected_weightfiles:
        for v in validation_loss_files:
            if fname(s) in v:
                o = lo(v)
                V[fname(s)]['lst'] += o

    validation_losses = range(len(selected_weightfiles))
    for a in V.keys():
        validation_losses[V[a]['ctr']] = np.mean(na(V[a]['lst']))

    clf()
    plot(validation_losses,'k.-')
    plt.title(d2s('validation of',network_to_validate))
    plt.ylabel('loss')
    plt.xlabel('weightfiles')
    plt.xlim(0,300)
    spause()
    return V,validation_losses


if __name__ == '__main__':
    Defaults = {
        'data':0,
        'curve':0,
        'network_to_validate':'Sq120_ldr_output_4April2019',
        'num':50,
    }
    setup_Default_Arguments(Defaults)
    print_Arguments()
    if Arguments['data']:
        get_validation_data(
            Arguments['network_to_validate'],
            Arguments['num'],
        )

    if Arguments['curve']:
        get_validation_curve(
            Arguments['network_to_validate'],
        )
        raw_enter()

if False:


    o=lo('/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/data_moments_dic.pkl')
    #,a
    I = {}
    ctr = 0
    for x in ['train']:#,'val']:
        for y in ['high_steer']:#,'low_steer','reverse']:
                R = o['train'][y]
                for A in R:
                    if A['run_name'] == 'tegra-ubuntu_15Nov18_20h52m26s':
                        ctr += 1
                        i = A['left_ts_index'][1]
                        if i not in I:
                            I[i] = 0
                        I[i] += 1
    print ctr
    l = []
    for i in sorted(I.keys()):
        l.append(I[i])
    clf();plot(l,'.')


M = {}
steer_types = _data_moments_indexed['train'].keys() # i.e., high_steer, low_steer, reverse
for k in steer_types:
    M[k] = _data_moments_indexed['train'][k] + _data_moments_indexed['val'][k]
steer_types = M.keys()
equalize_to_max_len(M)

def equalize_to_max_len(M):
    cg("equalize_to_max_len()")
    cg("\tinitial lengths:")
    for k in M.keys():
        cg("\t\t",k,len(M[k]))
    lens = []
    steer_types = M.keys()

    for k in steer_types:
        lens.append(len(M[k]))
    max_len = max(lens)

    for k in steer_types:
        if len(M[k]) == 0:
            continue
        while len(M[k]) < max_len:
            random.shuffle(M[k])
            M[k] += M[k]
            if len(M[k]) > max_len:
                M[k] = M[k][:max_len]

    for k in steer_types:
        assert (len(M[k]) == max_len) or (len(M[k]) == 0)
    cg("\tfinal lengths:")
    for k in M.keys():
        cg("\t\t",k,len(M[k]))


B = {}
B['left'] = []
B['right'] = []
B['direct'] = []

for k in steer_types:
    for _dm in M[k]:
        if _dm['behavioral_mode'] == 'center':
            _dm['behavioral_mode'] = 'direct'
        if _dm['motor'] > 53 or (_dm['behavioral_mode'] == 'direct' and fname(e) == 'left_direct_stop'):

            if _dm['behavioral_mode'] in B:
                B[_dm['behavioral_mode']].append(_dm)
            else:
                pass #cr("behavioral_mode not in B: ",_dm['behavioral_mode'])
equalize_to_max_len(B)
P = {}
P['data_moments_indexed'] = []
for b in B.keys():
    P['data_moments_indexed'] += B[b]
random.shuffle(P['data_moments_indexed'])

#,b


if 'N' not in locals():
    N = lo(opjD('Data/Network_Predictions',('tegra-ubuntu_30Oct18_15h58m09s.net_predictions.pkl')))
if False:
    for i in range(10000,20000):
        clf()
        plt.xlim(-60,60)
        for c,t in zip(['r','b','g'],['left','direct','right']):
            plot(-N[t][i]['heading'],rlen(N[t][i]['heading']),c+'.-')
        a = N['left'][i]['heading']
        b = N['direct'][i]['heading']
        d = -(a+b)/2.
        plot(d,rlen(d),'k.-')    
        plt.title(d2s(i))
        spause()
        time.sleep(1/30.)


P = {}

P['ABORT'] = False
P['customers'] = ['VT menu']
P['To Expose'] = {}
#
###############################################3

# walking pace ~= 1.4 m/s
P['graphics 1'] = True ####TEMP_CHANGE False
P['graphics 2'] = True
P['graphics 3'] = True ####TEMP_CHANGE False
P['save metadata'] = False
P['step_size'] = 1
P['cmd/clear_screen'] = False
P['cv2 delay'] = 1
P['3d image scale'] = 2.0#1.0
P['metadata_3D_img scale'] = 8.3
P['Prediction2D_plot scale'] = 8.3
P['num timesteps'] = 2#8
P['load_timer_time'] = 2
P['U_heading_gain'] = 2.0
P['initial index'] = 0
P['backup parameter'] = 1.0
P['use center line'] = True
P['cmd/an impulse (click)'] = False
P['show timer time'] = 0
P['add_mode'] = True
P['skip_3D'] = False
P['d_heading_multiplier'] = 1.0
P['cmd_camera_to_camera_heading_cooeficient'] = 0.75
P['99 mov timer time'] = 1.0
P['To Expose']['VT menu'] = sorted(P.keys())
to_hide = ['To Expose','customers']
for h in to_hide:
    P['To Expose']['VT menu'].remove(h)
for k in P.keys():
    if '!' in k:
        P['To Expose']['VT menu'].remove(k)
P['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
P['timer'] = Timer(5)
P['vec sample frequency'] = 3.33
P['start menu automatically'] = False
P['vel-encoding coeficient'] = (1.0/2.3)
P['show timer'] = Timer(P['show timer time'])
P['wait for start signal'] = False
P['index'] = P['initial index']
P['topic_suffix'] = ''
P['behavioral_mode_list'] = ['left','direct','right']


def vec(heading,encoder,motor,sample_frequency,_):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

def get_predictions2D(headings,encoders,motors,sample_frequency,_):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],P['vec sample frequency'],_) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step
Q = N['left'][10000]
pts = get_predictions2D(Q['heading'],Q['encoder'],Q['motor'],30,{})
clf();xylim(-1,1,0,2)
pts_plot(pts)


#EOF
