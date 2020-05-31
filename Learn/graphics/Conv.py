from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None
#W = {}


def parse_target_vector(v,reverse=False):
    #print shape(v)
    q = 66#42
    assert len(v) == 6*q
    lx = v[0:q]
    rx = v[q:2*q]
    ly = v[2*q:3*q] * 10
    ry = v[3*q:4*q] * 10
    al = v[4*q:5*q] * 10
    ar = v[5*q:6*q] * 10
    if reverse:
        lx *= -1
        rx *= -1
        al *= -1
        ar *= -1
    outer_countours_rotated_left = zeros((q,2))
    outer_countours_rotated_left[:,0] = lx
    outer_countours_rotated_left[:,1] = ly

    outer_countours_rotated_right = zeros((q,2))
    outer_countours_rotated_right[:,0] = rx
    outer_countours_rotated_right[:,1] = ry

    angles_left = al
    angles_right = ar

    return outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right,

Colors = {'direct':'b','left':'r','right':'g'}

def plot_map(
    outer_countours_rotated_left,
    outer_countours_rotated_right,
    angles_left,
    angles_right,
    color='k',
    name='map',
    e = 24,
    marker_size_divisor = 4.0,
):
    D = {
            'angles' : {
                'left' :     angles_left,
                'right' :    angles_right,
            },
            'outer_countours_rotated' : {
                'left' :     outer_countours_rotated_left,
                'right' :    outer_countours_rotated_right,
            },
            'marker_size' : {
                'left' :     angles_left,
                'right' :    angles_right,
            },
            #'turns' : M['turns'][i].copy(),
    }

    for k in ['left','right']:
        for l in rlen(D['marker_size'][k]):
            a = min(np.abs(D['marker_size'][k][l]),80)
            marker_size = int(a/marker_size_divisor)
            D['marker_size'][k][l] = marker_size
 

    if 'plot rotated' and 'outer_countours_rotated' in D:
        
        figure(name); plt_square(); xylim(-e,e,-e/4,2*e)
        for k in ['left','right']:
            xy = D['outer_countours_rotated'][k]
            plot(xy[:,0],xy[:,1],color+'-',linewidth=1)
            for r in rlen(D['outer_countours_rotated'][k]):
                pts_plot(D['outer_countours_rotated'][k][r],Colors[k],sym='.',ms = D['marker_size'][k][r])





def graphics_function(N,M,P):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
        graphics_timer.trigger()

    cv2.waitKey(1)
    if graphics_timer.time_s != M['Q']['runtime_parameters']['graphics_timer_time']:
        graphics_timer.trigger()
    if graphics_timer.check() or M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
        if M['Q']['runtime_parameters']['graphics_timer_time'] == -2:
            raw_enter()
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    title_name = title='.'.join(P['type'])

    if True:
        
        figure(P['type'][-1],figsize=(2,10))
        clf()

        n = int(M['Q']['runtime_parameters']['percent_loss_to_show']/100.0 * len(N.losses))
        plot(N.losses[-n:],'.')
        m = meo(na(N.losses[-n:]),M['Q']['runtime_parameters']['meo_num'])
        plot(m)
        mm = na(m[int(len(m)/2):])
        mn,mx = 0,1
        if len(M['Q']['runtime_parameters']['graphics_ylim']) == 2:
            mn = M['Q']['runtime_parameters']['graphics_ylim'][0]
            mx = M['Q']['runtime_parameters']['graphics_ylim'][1]
            #print mn,mx
        elif len(mm) > 5 :
            #av = mm.mean()
            av=0
            std = mm.std()
            #mx = (mm.max()-av) * 1.3# + av
            #mn = (mm.min()-av) * 0.8# + av
            mn = mm.mean()-std*M['Q']['runtime_parameters']['loss_stds']
            mx = mm.mean()+std*M['Q']['runtime_parameters']['loss_stds']
        #print(std,mn,mx)
        if type(mn) == float and type(mx) == float:
            ylim(
                mn,
                mx,
            )

    Imgs = {}
    img_lst = []
    img_spacer = False
    k_prev = 'input'
    for k in ['input']:#,'output','target']:
        Imgs[k] = N.extract(k)

        if 'display.'+k in P:
            lst = P['display.'+k]
            for i in range(0,len(lst),2):
                start = int(lst[i])
                stop = int(lst[i+1])
                img = Imgs[k][start:stop,:,:]
                img = z55(img.transpose(2,1,0))
                if False:#k == 'input':
                    r = img[:,:168,0].copy()
                    g = img[:,:168,1].copy()
                    b = img[:,:168,2].copy()
                    img[:,:168,0] = b
                    img[:,:168,1] = g
                    img[:,:168,2] = r

                if k_prev != k:
                    k_prev = k
                    if type(img_spacer) == type(False):
                        img_spacer = 255+0*img[:,:10,:]
                    img_lst.append(img_spacer)

                img_lst.append(img)


    output_2 = N.extract('output_2')
    target = N.extract('target')
    meta = N.extract('meta')

    figure('target-output',figsize=(4,3));clf();
    plot(output_2,'r.')
    plot(target,'k.')


    if 'mapping1':
        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(target)

        figure('map');clf()

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='k',
            name='map',
            e = 19,
            #x_offset=-0,
        )

        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(output_2)

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='b',
            name='map',
            e = 19,
            #x_offset=0,
        )



        import kzpy3.Array.fit3d as fit3d
        
        figure('map3d');clf()#;plt_square();xylim(0,168,0,94)
        im = N.extract('input')
        im = z55(im.transpose(2,1,0))
        mi(im,'map3d')
        c = []
        for i in rlen(outer_countours_rotated_left):
            a = outer_countours_rotated_left[i,:]
            b = fit3d.point_in_3D_to_point_in_2D(
                a,
                height_in_pixels = 94,
                width_in_pixels = 168,
                backup_parameter=1,
            )
            c.append(b)
        c =na(c)
        #c[:,1] = 94-c[:,1]
        pts_plot(c,color='r',sym='.-')

        c = []
        for i in rlen(outer_countours_rotated_right):
            a = outer_countours_rotated_right[i,:]
            b = fit3d.point_in_3D_to_point_in_2D(
                a,
                height_in_pixels = 94,
                width_in_pixels = 168,
                backup_parameter=1,
            )
            c.append(b)
        c =na(c)
        #c[:,1] = 94-c[:,1]
        pts_plot(c,color='g',sym='.-')


        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(target)

        figure('map target');clf()

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='k',
            name='map target',
            e = 19,
            #x_offset=-0,
        )

        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(output_2)

        figure('map output_2');clf()

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='b',
            name='map output_2',
            e = 19,
            #x_offset=0,
        )





    figure('meta',figsize=(3,3))
    meta[4,0,0] = 1
    meta[4,0,1] = 2
    meta[4,0,2] = 3
    mi(meta[4,:,:],'meta')

    if False:
        meta = N.extract('meta')
        for i in range(5):
            mi(meta[i,:,:],i)
    spause()

    concatt = None
    while len(img_lst) > 0:
        img = img_lst.pop(0)
        if type(concatt) == type(None):
            concatt = img.copy()
            #print 'a',shape(concatt),shape(img)
        else:
            #print 'b',shape(concatt),shape(img)
            concatt = np.concatenate((concatt,img),axis=1)
    mci(concatt,1,scale=M['Q']['runtime_parameters']['scale'],title=title_name)


    if M['Q']['runtime_parameters']['save_images']:
        path = opjD('__TEMP__',fname(P['NETWORK_OUTPUT_FOLDER']))
        print path
        os.system(d2s('mkdir -p',path))
        imsave(opj(path,str(time.time())+'.png'),img)


    spause()



#EOF



