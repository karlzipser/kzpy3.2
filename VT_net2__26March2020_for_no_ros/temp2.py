



#,a
if 'L' not in locals():
    L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
    cm('opened L')

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


start = 6800
stop = 12000



xy = na([na([0,0])])

print_timer = Timer(0.1)

alpha,alpha_prev = 0,0
#a_prev = [0,1]
dalpha = []
for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    #a_prev = a
    a = vec(L['gyro_heading_x_meo'][i],L['encoder_meo'][i],L['motor'][i])
    #print a,i



    xy = np.concatenate((xy,na([a+xy[-1]])))

    alpha_prev = alpha
    alpha = get_alpha(na(xy[-2:,:]))

    dalpha.append(alpha-alpha_prev)
    
    d_alpha = alpha-alpha_prev

    print i,dp(alpha)

    b = rotate_alpha(90-alpha,[a])#,xy)


    xy -= xy[-2]

    if True:#print_timer.check():
        if True:
            figure(1)
            clf()
            pts_plot(xy,sym='.-')
            plt_square()
            #time.sleep(1)

        figure(2)
        clf()
        #plot([0,a_prev[0]],[0,a_prev[1]],'c:')
        plot([0,a[0]],[0,a[1]])
        plot([0,b[0][0]],[0,b[0][1]])
        plt_square(0.125)

        figure(3)
        clf()
        plot([0,len(dalpha)],[0,0],'k:')
        plot(dalpha[1:],'.-')
        ylim(-5,5)

        spause()

#,b


#EOF

