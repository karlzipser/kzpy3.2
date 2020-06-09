
#,a

Arguments['run'] = 'Mr_Black_24Sep18_18h52m26s'#'tegra-ubuntu_31Oct18_16h06m32s'  # 

if len(sggo(opjD('Data/train/h5py',Arguments['run']))) > 0:
    run_type = 'train'
elif len(sggo(opjD('Data/validate/h5py',Arguments['run']))) > 0:
    run_type = 'validate'
else:
    clp(Arguments['run'],'not found')
    assert False

if 'startup material':

    if 'L' not in locals():
        L=h5r(opjD('Data',run_type,'h5py',Arguments['run'],'left_timestamp_metadata_right_ts.h5py'))
        cm('opened L')
        O = h5r(opjD('Data',run_type,'h5py',Arguments['run'],'original_timestamp_data.h5py'))
        cm('opened O')
    """
    if 'T' not in locals():
        T = h5r(opjD('Data/outer_contours/rotated2',Arguments['run']+'.h5py'))
    """
    if 'Y' not in locals():
        Y = lo(opjD('Data/outer_contours/output_2_data',run_type,Arguments['run']+'.pkl'))

    start = 0
    stop = 30000 #len(L['motor'])
    print_timer = Timer(1/70.)
    alpha = 0
    xyi = na([[0,0,0]])
    sample_frequency = 30





    """
    if 'UT' not in locals():
        cm('Building UT...')
        t0 = time.time()
        UT = {
            'past':{
                'range':(23,24),
                'back_steps':30*sample_frequency,
                'S':{},
            },
            'future':{
                'range':(21,66),
                'back_steps':2,
                'S':{},
            },
        }

        for k in ['past','future']:
            a,b = UT[k]['range']
            for i in range(start,stop,1):
                UT[k]['S'][i] = {
                    'left': T['outer_countours_rotated_left'][i,a:b,:],
                    'right':  T['outer_countours_rotated_right'][i,a:b,:],
                    'index':i,
                    'steps_left':0,
                }
        soD(UT,'UT')
        cm('Made UT in',dp(time.time()-t0),'seconds')
    else:
        t0 = time.time()
        UT = loD('UT')
        cm('in',time.time()-t0,'seconds')
    """





    if 'UO' not in locals():
        cm('Building UO...')
        t0 = time.time()
        UO = {
            'past':{
                'range':(21,26),#(23,24),
                'back_steps':30*sample_frequency,
                'S':{},
            },
            'future':{
                'range':(21,66),
                'back_steps':5,
                'S':{},
            },
        }

        for k in ['past','future']:
            a,b = UO[k]['range']
            for i in range(start,stop,1):
                if i not in Y:
                    continue
                UO[k]['S'][i] = {
                    'left': Y[i]['outer_countours_rotated_left'][a:b,:],
                    'right':  Y[i]['outer_countours_rotated_right'][a:b,:],
                    'index':i,
                    'steps_left':0,
                }
        soD(UO,'UO')
        cm('Made UO in',dp(time.time()-t0),'seconds')
    else:
        t0 = time.time()
        UO = loD('UO')
        cm('in',time.time()-t0,'seconds')



if 'vector functions':

    def vec(heading,encoder,motor,sample_frequency=30.,vel_encoding_coeficient=1.0/2.6): #2.3): #3.33
        velocity = encoder * vel_encoding_coeficient # rough guess
        if motor < 49:
            velocity *= -1.0
        a = [0,1]
        a = array(rotatePoint([0,0],a,heading))
        a *= velocity/sample_frequency
        return array(a)


    def line_function(x,A,B):
        return A*x+B


    def get_alpha(xy):
        if type(xy) == list or type(xy) == tuple:
            xy = na(xy)
        m,b = curve_fit(line_function,xy[:,0],xy[:,1])[0]
        alpha = corrected_angle(m,xy[-1,:],xy[0,:])
        return alpha


    def rotate_alpha(alpha,xy):
        xy_rotated = rotatePolygon( xy, alpha)
        return xy_rotated


    def magnitude(a):
        return np.sqrt(a[0]**2+a[1]**2)


    def dist(A,B):
        return np.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )


    def distance_decimate_vector(v,d):
        ref = v[0,:]
        u = [ref]
        for i in range(0,len(v)-1):
            e = dist(v[i],v[i+1])
            if dist(ref,v[i]) >= d:
                ref = v[i]
                u.append(ref)
        u.append(v[-1])
        return na(u)

PATH = [na([0,0])]

def grow_path(heading,encoder,motor,xyi,alpha,i,back_steps):

    a = vec(heading,encoder,motor)
    PATH.append(PATH[-1]+a)


    if len(xyi) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        d_alpha = alpha - alpha_prev

        xy = xyi[:,:2]

        xy -= xy[-1]

        xyi[:,:2] = xy


        xyi[:,:2] = rotate_alpha(d_alpha, xyi[:,:2])

    else:
        d_alpha = 0

    xyi = np.concatenate((xyi, na([[ 0, magnitude(a), i ]])))

    if len(xyi) > back_steps:
        xyi = xyi[-back_steps:]

    return xyi,alpha,d_alpha,a


times = {
    'grow_path':[],
    'past_future':[],
    'graphics':[],
}
times_mean = {
    'grow_path':0,
    'past_future':0,
    'graphics':0,
}


U = UO


for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        continue

    t0 = time.time()
    xyi,alpha,d_alpha,a = grow_path(
        L['gyro_heading_x_meo'][i],
        L['encoder_meo'][i],
        L['motor'][i],
        xyi,
        alpha,
        i,
        1 * sample_frequency,
    )

    times['grow_path'].append(time.time()-t0)


    t0 = time.time()

    for k in ['past','future']:

        S = U[k]['S']

        for j in S:

            if j > i:
                continue

            R = S[j]

            if R['index'] == i:

                R['steps_left'] = U[k]['back_steps']


            if R['steps_left']:

                R['steps_left'] -= 1

                for s in ['left','right']:

                    R[s] -= na([[0,magnitude(a)]])
                    R[s] = rotate_alpha(d_alpha, R[s])

                assert R['steps_left'] >= 0

                

    times['past_future'].append(time.time()-t0)


    if 'graphics':
        t0 = time.time()
        e = 100
        if i % 30 == 0:
            xy = xyi[:,:2]
            figure(1)
            clf()
            plot([-e,e],[0,0],'k:')
            plot([0,0],[-e,e],'k:')
            pts_plot(xy,sym='.',color='c',ms=4)
            for k in ['past','future']:
                S = U[k]['S']
                for j in S:
                    R = S[j]
                    if R['steps_left']:
                        pts_plot(R['left'],sym='.',ms=2,color='r')
                    if R['steps_left']:
                        pts_plot(R['right'],sym='.',ms=2,color='g')

            xylim(-50,50,-50,30)
            plt_square()
            plt.title(i)
            spause()
            mci(O['left_image']['vals'][i],title='left_image')

            if len(PATH) > 30:
                figure(10)
                clf()
                plt_square()
                pts_plot(PATH[0:len(PATH):30],color='k')

    times['graphics'].append(time.time()-t0)
    

    if i % 100 == 0:
        for k in times.keys():
            times_mean[k] = na(times[k]).mean()
        kprint(times_mean,'times_mean')


#,b


#EOF

