
#,a


if 'startup material':

    if 'L' not in locals():
        L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
        cm('opened L')

    if 'T' not in locals():
        T = h5r(opjD('Data/outer_contours/rotated2/tegra-ubuntu_31Oct18_16h06m32s.h5py'))

    start = 6500
    stop = len(L['motor'])#12000
    print_timer = Timer(1/70.)
    back_steps = 30*10
    alpha = 0
    xyi = na([[0,0,0]])

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

    def distance_decimate_vector_with_indicies(v,d):

        ref = v[0,:]
        u = [ref]
        for i in range(0,len(v)-1):
            #e = dist(v[i,:2],v[i+1,:2])
            if dist(ref[:2],v[i,:2]) >= d:
                ref = v[i]
                u.append(ref)
        u.append(v[-1])
        return na(u)

def grow_path(heading,encoder,motor,xyi,alpha,i,back_steps):

    a = vec(heading,encoder,motor)

    if len(xyi) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        d_alpha = alpha - alpha_prev

        xy = xyi[:,:2]

        xy -= xy[-1]

        xyi[:,:2] = rotate_alpha(d_alpha, xy)

        print shape(xyi)
    else:
        d_alpha = 0

    xyi = np.concatenate((xyi, na([[ 0, magnitude(a), i ]])))

    if len(xyi) > back_steps:
        xyi = xyi[-back_steps:]

    return xyi,alpha,d_alpha,a




if True:
    U = {
        'past':{
            'range':(23,24),
            'back_steps':back_steps,
            'S':{},
        },
        'future':{
            'range':(21,66),
            'S':{},
            'back_steps':2,
        },
    }

    for k in ['past','future']:
        a,b = U[k]['range']
        for i in range(start,12000,1):
            #print i
            U[k]['S'][i] = {
                'left': T['outer_countours_rotated_left'][i,a:b,:],
                'right':  T['outer_countours_rotated_right'][i,a:b,:],
                'index':i,
                'back_steps':U[k]['back_steps'],
                'steps_left':0,
            }


Ctr = {}
ctr = start

for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        continue

    Ctr[i] = ctr
    ctr += 1

    xyi,alpha,d_alpha,a = grow_path(
        L['gyro_heading_x_meo'][i],
        L['encoder_meo'][i],
        L['motor'][i],
        xyi,
        alpha,
        i,
        back_steps,
    )

    for k in ['past','future']:
        S = U[k]['S']
        for j in S:

            R = S[j]

            if R['index'] == i:
                R['steps_left'] = R['back_steps']


            if R['steps_left']:

                R['steps_left'] -= 1

                for s in ['left','right']:

                    R[s] -= na([[0,magnitude(a)]])
        
                    #R[s] = distance_decimate_vector(R[s],5)

                    R[s] = rotate_alpha(d_alpha, R[s])

            assert R['steps_left'] >= 0



    if 'graphics':
        e = 100
        if i % 15 == 0:
            cy(i)
            xy = xyi[:,:2]
            figure(1)
            clf()
            plot([-e,e],[0,0],'k:')
            plot([0,0],[-e,e],'k:')
            pts_plot(xy,sym='.-',color='c',ms=1)
            for k in ['past','future']:
                S = U[k]['S']
                for j in S:
                    R = S[j]
                    if R['steps_left']:
                        pts_plot(R['left'],sym='.',ms=2,color='r')
                    if R['steps_left']:
                        pts_plot(R['right'],sym='.',ms=2,color='g')

            xylim(-25,25,-50,25)
            plt_square()

            figure(2)
            clf()
            plot([-e,e],[0,0],'k:')
            plot([0,0],[-e,e],'k:')
            pts_plot(xy,sym='.-',color='c',ms=2)

            for k in ['past','future']:#U:
                S = U[k]['S']
                for j in S:
                    R = S[j]
                    if R['steps_left']:
                        pts_plot(R['left'],sym='.',ms=3,color='r')
                    if R['steps_left']:
                        pts_plot(R['right'],sym='.',ms=3,color='g')

            xylim(-12,12,-24,24)
            plt_square()

            spause()



#,b


#EOF

