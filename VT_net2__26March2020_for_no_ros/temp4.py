
#,a
if False:
    P={}
    print('#############\n#')

    for r in All_runs['train']:
        q = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)
        if 'h5py' in q['parent_folders']:
            a = q['src']
            b = a_key(q['paths'])
            c = q['paths'][b][0]
            P[r] = opj(a,b,c)
    print('#\n#############\n')
    for r in P:
        print P[r]

if 'startup material':

    if 'L' not in locals():
        L=h5r('/Users/karlzipser/Desktop/Data/X/h5py/tegra-ubuntu_31Oct18_16h06m32s/left_timestamp_metadata_right_ts.h5py')
        cm('opened L')

    start = 0#6500
    stop = len(L['motor'])#12000
    print_timer = Timer(1/20.)
    back_steps = 30*10

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


def grow_path(heading,encoder,motor,xy,alpha,other=None,back_steps=None):

    a = vec(heading,encoder,motor)

    a_mag = np.sqrt(a[0]**2+a[1]**2)

    if len(xy) > 1:

        alpha_prev = alpha
        alpha = 90 - get_alpha([[0,0],a])

        other += xy[-1]
        
        xy -= xy[-1]

        xy = rotate_alpha((alpha - alpha_prev), xy)
        if other is not None:
            
            other = rotate_alpha((alpha - alpha_prev), other)

    xy = np.concatenate((xy,na([[0,a_mag]])))

    if back_steps is not None and len(xy) > back_steps:
        xy = xy[-back_steps:]

    return xy,alpha,other




alpha = 0
xy = na([[0,0]])
other = rnd((5,2))

for i in range(start,stop):

    if not L['drive_mode'][i]:
        continue

    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        continue


    xy,alpha,other = grow_path(
        L['gyro_heading_x_meo'][i],
        L['encoder_meo'][i],
        L['motor'][i],
        xy,
        alpha,
        other,
        back_steps,
    )


    if print_timer.check():

        figure(1)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        xylim(-50,50,-100,3)
        plt_square()

        figure(2)
        clf()
        pts_plot(xy,sym='.-',ms=2)
        pts_plot(other,sym='.-',ms=2,color='b')
        xylim(-1,1,-2,0.1)
        plt_square()

        spause()
        #raw_enter()
        print_timer.reset()

#,b


#EOF

