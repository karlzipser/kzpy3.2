



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



xy = na([na([0,1])])



alpha,alpha_prev = 0,0

dalpha = []

for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue


    a = vec(L['gyro_heading_x_meo'][i],L['encoder_meo'][i],L['motor'][i])

    a_mag = np.sqrt(a[0]**2+a[1]**2)

    alpha_prev = alpha

    if len(xy) > 1:

        alpha = get_alpha(xy[-2:,:])
        print alpha,alpha - alpha_prev,xy[-2:,:]
        xy -= xy[-1]
        xy = rotate_alpha(90 - (alpha - alpha_prev), xy)

    xy = np.concatenate((xy,na([[0,a_mag]])))

    

    if True:
        figure(1)
        clf()
        pts_plot(xy,sym='.-')
        plt_square()

        spause()

#,b


#EOF

