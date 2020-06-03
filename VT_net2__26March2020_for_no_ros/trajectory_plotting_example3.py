
#,a


if 'startup material':

    if 'L' not in locals():
        L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
        cm('opened L')

    if 'T' not in locals():
        T = h5r(opjD('Data/outer_contours/rotated2/tegra-ubuntu_31Oct18_16h06m32s.h5py'))

    start = 4000#6500
    stop = len(L['motor'])#12000
    print_timer = Timer(1/70.)
    back_steps = 300#30*60
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



def grow_path(heading,encoder,motor,xyi,alpha,i):

    a = vec(heading,encoder,motor)

    if len(xyi) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        d_alpha = alpha - alpha_prev

        xy = xyi[:,:2]

        xy -= xy[-1]

        xyi[:,:2] = rotate_alpha(d_alpha, xy)

    else:
        d_alpha = 0

    xyi = np.concatenate((xyi, na([[ 0, magnitude(a), i ]])))

    if len(xyi) > back_steps:
        xyi = xyi[-back_steps:]

    return xyi,alpha,d_alpha,a


S = {}
for i in range(5000,7000,10):
    S[i] = {
        'left': T['outer_countours_rotated_left'][i,12:14,:],    #2*rndn(10,2)-na([1,0]),
        'right':  T['outer_countours_rotated_right'][i,12:14,:],  #1*rndn(10,2)+na([1,0]),
        'index':i,
        'active':False
    }



for i in range(start,stop):
    print i
    if not L['drive_mode'][i]:
        cr(i)
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        cr(i)
        continue

    xyi,alpha,d_alpha,a = grow_path(
        L['gyro_heading_x_meo'][i],
        L['encoder_meo'][i],
        L['motor'][i],
        xyi,
        alpha,
        i,
    )


    for j in S:
        R = S[j]

        if R['index'] == i:
            R['active'] = True
            cy(i,'activated')


        if R['active']:
            if R['index'] + back_steps < xyi[-1,2]:
                R['active'] = False
                cb(j,'inactivated')


        if R['active']:
            for s in ['left','right']:
                R[s] -= na([[0,magnitude(a)]])
                R[s] = rotate_alpha(d_alpha, R[s])







    if 'graphics':
        if i % 2 == 0:
            xy = xyi[:,:2]
            figure(1)
            clf()
            pts_plot(xy,sym='.-',color='c',ms=1)
            for j in S:
                R = S[j]
                if R['active']:
                    pts_plot(R['left'],sym='.',ms=2,color='r')
                if R['active']:
                    pts_plot(R['right'],sym='.',ms=2,color='g')
            xylim(-25,25,-50,3)
            plt_square()

            figure(2)
            clf()
            pts_plot(xy,sym='.-',color='c',ms=2)

            for j in S:
                R = S[j]
                if R['active']:
                    pts_plot(R['left'],sym='.',ms=2,color='r')
                if R['active']:
                    pts_plot(R['right'],sym='.',ms=2,color='g')

            xylim(-1,1,-2,0.1)
            plt_square()

            spause()



#,b


#EOF

