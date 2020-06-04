from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None
#W = {}
e = 24


if 'rotate in 3d':
    #https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
    import numpy as np
    import math

    def rotation_matrix(axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

    v = [3, 5, 0]
    axis = [4, 4, 1]
    theta = 1.2 

    print(np.dot(rotation_matrix(axis, theta), v)) 
    # [ 2.74911638  4.77180932  1.91629719]





def double_interp_1D_array(a):
    b = []
    for i in range(len(a)-1):
        c = a[i]
        d = a[i+1]
        e = (c+d)/2.0
        b.append(c)
        b.append(e)
    b.append(a[-1])
    return na(b)

def double_interp_2D_array(a):
    b = double_interp_1D_array(a[:,0])
    c = double_interp_1D_array(a[:,1])
    d = zeros((len(b),2))
    d[:,0] = b
    d[:,1] = c
    return d

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
    grid=True,
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
        
        figure(name); plt_square(); xylim(-e,e,-e,e)

        if grid:
            plot([-e,e],[0,0],'k:')
            plot([0,0],[-e,e],'k:')

        for k in ['left','right']:
            xy = D['outer_countours_rotated'][k]
            plot(xy[:,0],xy[:,1],color+'-',linewidth=1)
            for r in rlen(D['outer_countours_rotated'][k]):
                pts_plot(D['outer_countours_rotated'][k][r],Colors[k],sym='.',ms = D['marker_size'][k][r])



def k_in_D(k,D):
    if k not in D:
        return False
    else:
        return D[k]

fig_path = opjD('Data/outer_contours/figures')
os.system('mkdir -p '+fig_path)

def graphics_function(N,M,P):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
        graphics_timer.trigger()

    cv2.waitKey(1)
    if graphics_timer.time_s != M['Q']['runtime_parameters']['graphics_timer_time']:
        graphics_timer.trigger()

    if 'save_figures' in P:
        if P['save_figures'] > 0:
            cb("P['save_figures'] =",P['save_figures'])
            time_string = d2p(P['run'],P['ctr'])
            graphics_timer.trigger()
            P['save_figures'] -= 1
            if P['save_figures'] < 0:
                P['save_figures'] = 0
        else:
            cg('done saving figures')
            sys.exit(0)

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
            e=e,
            grid=True,
        )

        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(output_2)

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='b',
            name='map',
            e=e,
            grid=False,
        )

        if k_in_D('save_figures',P):
            plt.savefig(opj(fig_path,d2p(time_string,'map','pdf')),format='pdf')






        import kzpy3.Array.fit3d as fit3d

        im = N.extract('input')
        im = z55(im.transpose(2,1,0))

        for data,name in ((output_2,'output_2'),(target,'target')):

            outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(data)
            figname = 'map3d-'+name
            figure(figname);clf()

            mi(im,figname)

            for o,color in ((outer_countours_rotated_left,'r'),(outer_countours_rotated_right,'g')):
                c = []
                w = double_interp_2D_array(o[:33,:])
                w = double_interp_2D_array(w)
                w = double_interp_2D_array(w)
                o = np.concatenate((w,o[33:,:]))

                for i in rlen(o):
                    a = o[i,:]
                    b = fit3d.point_in_3D_to_point_in_2D(
                        a,
                        height_in_pixels = 94,
                        width_in_pixels = 168,
                        backup_parameter=1,
                    )
                    if False not in b:
                        c.append(b)
                c = na(c)
                try:
                    pts_plot(c,color=color,sym='.')
                except:
                    clp('Exception, shape(c) =',shape(c),'`wrb')

            if k_in_D('save_figures',P):
                plt.savefig(opj(fig_path,d2p(time_string,figname,'pdf')),format='pdf')



        outer_countours_rotated_left, outer_countours_rotated_right, angles_left, angles_right = parse_target_vector(target)

        figure('map target');clf()

        plot_map(
            outer_countours_rotated_left,
            outer_countours_rotated_right,
            angles_left,
            angles_right,
            color='k',
            name='map target',
            e=e,
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
            e=e,
            #x_offset=0,
        )
        cg(P['ctr'])
        if k_in_D('save_figures',P):
            plt.savefig(opj(fig_path,d2p(time_string,'map_output_2','pdf')),format='pdf')






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

    if k_in_D('save_figures',P):
        plt.savefig(opj(fig_path,d2p(time_string,'meta','pdf')),format='pdf')


    if M['Q']['runtime_parameters']['save_images']:
        path = opjD('__TEMP__',fname(P['NETWORK_OUTPUT_FOLDER']))
        print path
        os.system(d2s('mkdir -p',path))
        imsave(opj(path,str(time.time())+'.png'),img)


    spause()

    #if k_in_D('save_figures',P):
    #    cm('ready to save figure',ra=1)


#EOF



