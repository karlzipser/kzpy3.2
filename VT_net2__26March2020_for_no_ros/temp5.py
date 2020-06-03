
#,a


if 'startup material':

    if 'L' not in locals():
        L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
        cm('opened L')

    start = 0#6500
    stop = len(L['motor'])#12000
    print_timer = Timer(1/70.)
    back_steps = 30*60


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



def _grow_path(heading,encoder,motor,xy,alpha,other,back_steps):

    a = vec(heading,encoder,motor)

    a_mag = np.sqrt(a[0]**2+a[1]**2)

    if len(xy) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        #other -= other[0]
        #other += xy[0]

        xy -= xy[-1]

        xy = rotate_alpha((alpha - alpha_prev), xy)

        #other = rotate_alpha((alpha - alpha_prev), other)

    xy = np.concatenate((xy,na([[0,a_mag]])))

    if len(xy) > back_steps:
        xy = xy[-back_steps:]

    return xy,alpha,other






def __grow_path(heading,encoder,motor,xy,alpha,back_steps,indicies,i):

    a = vec(heading,encoder,motor)

    if len(xy) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        d_alpha = alpha - alpha_prev

        xy -= xy[-1]

        xy = rotate_alpha(d_alpha, xy)
    else:
        d_alpha = 0

    xy = np.concatenate((xy, na([[ 0, magnitude(a) ]])))
    indicies.insert(0,i)

    if len(xy) > back_steps:
        xy = xy[-back_steps:]
        indicies = indicies[:back_steps]

    return xy,alpha,d_alpha,indicies



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

    return xyi,alpha,d_alpha




alpha = 0
xyi = na([[0,0,0]])


other = 2*rndn(100,2)
other_index = 4970
other_start = False

for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        continue


    xyi,alpha,d_alpha = grow_path(
        L['gyro_heading_x_meo'][i],
        L['encoder_meo'][i],
        L['motor'][i],
        xyi,
        alpha,
        i,
    )

    if other_index == i:
        other_start = True
    if other_index < indicies[0] and other_index > indicies[-2]:
        #other -= other[0]
        other -= xy[-1]
        other = rotate_alpha(d_alpha, other)
        show_other = True
    else:
        show_other = False
    """
    show_other = False
    
    xy = xyi[:,:2]

    if i % 60 == 0:#print_timer.check():
        print shape(xyi)
        figure(1)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        if show_other:
            pts_plot(other,sym='.',ms=2,color='b')
        xylim(-50,50,-100,3)
        plt_square()

        figure(2)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        if show_other:
            pts_plot(other,sym='.',ms=2,color='b')
        xylim(-1,1,-2,0.1)
        plt_square()

        spause()
        #raw_enter()

        #print other
        #print xyi
        #print_timer.reset()

        #raw_enter()

#,b


#EOF

