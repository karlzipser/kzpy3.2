
#,a




if 'L' not in locals():
    L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
    cm('opened L')

start = 0#6500
stop = len(L['motor'])#12000

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



print_timer = Timer(1/20.)

xy = na([[0,0]])

alpha,alpha_prev = 0,0


for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        continue

    a = vec(L['gyro_heading_x_meo'][i],L['encoder_meo'][i],L['motor'][i])

    a_mag = np.sqrt(a[0]**2+a[1]**2)

    if xy is None:
        xy = na([[0,a_mag]])
        
    else:
        if len(xy) > 1:

            alpha_prev = alpha
            alpha = 90 - get_alpha([[0,0],a])
            #print alpha,alpha - alpha_prev,xy[-2:,:]
            xy -= xy[-1]
            xy = rotate_alpha((alpha - alpha_prev), xy)

        xy = np.concatenate((xy,na([[0,a_mag]])))

    

    if print_timer.check():
        figure(1)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        xylim(-50,50,-100,3)
        plt_square()

        figure(2)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        xylim(-1,1,-2,0.1)
        plt_square()

        spause()
        #raw_enter()
        print_timer.reset()

#,b


#EOF

