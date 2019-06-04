from kzpy3.vis3 import *
import fit3d
exec(identify_file_str)

def Array(
    max_len,
    n_dims,
    name = None,
):

    D = {}
    D['max_len'] = max_len
    D['n_dims'] = n_dims
    D['data'] = zeros((2*max_len,n_dims+1+1))
    D['array'] = D['data'][:,:n_dims]
    D['keys'] = D['data'][:,-1]
    D['code'] = D['data'][:,n_dims]
    D['ctr'] = 0
    D['key_ctr'] = 0
    D['Dic'] = {}
    D['plot'] = None
    if name == None:
        name = d2s('plot',rnd())
    D['name'] = name



    def function_assign_plot(
        P
    ):
        assert dic_is_type(P,'CV2Plot')
        D['plot'] = P



    def function_setup_plot(
        height_in_pixels,
        width_in_pixels,
        pixels_per_unit,
        x_origin_in_pixels=None,
        y_origin_in_pixels=None,
    ):
        D['plot'] = CV2Plot(
            height_in_pixels,
            width_in_pixels,
            pixels_per_unit,
            x_origin_in_pixels,
            y_origin_in_pixels,
        )



    def function_check_len(
    ):
        ctr = D['ctr']
        max_len = D['max_len']
        if ctr > 1.5 * max_len:
            D['data'][:max_len,:] = D['data'][ctr - max_len:ctr,:]
            D['data'][-max_len:,:] = 0
            D['ctr'] = max_len
            if len(D['Dic'].keys()) > 0:
                kys = list(D['keys'])
                for k in D['Dic'].keys():
                    if k not in kys:
                        del D['Dic'][k]


    def function_check_ts(
        t,
    ):
        now = time.time()
        ctr = D['ctr']

        found = False
        for i in range(ctr):
            #cg(i,D['keys'][i],D['Dic'][D['keys'][i]])
            ts = D['Dic'][D['keys'][i]]['time']
            #print now,ts,now-ts,i
            #cm(dp(now - ts))
            if now - ts <= t:
                found = True
                break
        if found:
            #cm(ctr-i,i,ctr)
            D['data'][:ctr-i,:] = D['data'][i:ctr,:]
            D['data'][ctr-i:,:] = 0
            D['ctr'] = ctr-i
            if len(D['Dic'].keys()) > 0:
                kys = list(D['keys'])
                for k in D['Dic'].keys():
                    if k not in kys:
                        del D['Dic'][k]
        else:
            D['data'] *= 0
            D['ctr'] = 0
            for k in D['Dic'].keys():
                del D['Dic'][k]

    def function_append(
        a,
        code=0,
        dic_info=None,
    ):
        assert len(a) == D['n_dims']
        function_check_len()
        ctr = D['ctr']
        D['array'][ctr,:] = a
        D['keys'][ctr] = D['key_ctr']
        D['code'][ctr] = code
        if dic_info != None:
            D['Dic'][D['key_ctr']] = dic_info
        D['ctr'] += 1
        D['key_ctr'] += 1

    def function_pop():
        D['data'][ctr,:] = 0.
        D['ctr'] -= 1
        D['key_ctr'] -= 1      

    def function_rotate(
        deg
    ):
        rotatePolygon__array_version(
            D['array'],
            deg,
        )



    def function_zero(
    ):
        D['array'][:D['ctr'],:] -= D['array'][D['ctr']-1]



    def function_show(
        use_CV2_plot=True,
        use_CV2_circles = False,
        use_maplotlib=True,
        do_print=True,
        clear=True,
        color=(255,255,255),
        code=None,
        show=True,
        grid=True,
        scale=1.0,
        background_image=None
    ):
        mx = min(D['ctr'],D['max_len'])
        #cr(mx,D['ctr'],D['max_len'])
        
        if code == None:
            the_array = D['array'][:mx,:]
        else:
            the_array = D['array'][D['code']==code][:mx,:]

        if clear:
            if type(background_image) != type(None):
                #cg("1111111")
                assert shape(D['plot']['image']) == shape(background_image)
                D['plot']['image'] = background_image
                #mci(background_image,title='l')
            else:
                D['plot']['clear']()
                #cg("2222222")
        if grid:
            D['plot']['grid'](c=[127,63,0])

        if do_print:
            for j in rlen(D['array']):
                a = D['data'][j,:] 
                cg(int(a[2]),yl,(intr(a[0]),intr(a[1])),bl,int(a[3]),sf=0)

        if use_CV2_circles and use_CV2_plot:
            for i in range(shape(the_array)[0]):
                x,y = int(the_array[i,0]),int(the_array[i,1])
                y = D['plot']['height_in_pixels'] - y
                cv2.circle(
                    D['plot']['image'],
                    (x,y),
                    2,
                    color,
                    -1
                )
        else:
            D['plot']['pts_plot'](the_array,c=color)

        if show:
            D['plot']['show'](title=D['name'],scale=scale)

        if use_maplotlib:
            if clear:
                clf()
            pts_plot(the_array,color=rndchoice(['r','g','k','b','m','c']))
            if show:
                plt_square()
                spause()


    def function_to_3D(A,backup_parameter=1.,min_dist=0.):
        D['ctr'] = 0
        D['data'] *= 0
        for j in range(A['ctr']):
            code = A['code'][j]
            dic_info = A['Dic'][A['keys'][j]]
            a = A['array'][j,:]
            #if 'a_prev' in locals():
            #    dist = np.sqrt((a[0]-a_prev[0])**2+(a[1]-a_prev[1])**2)
            #    cy(D['ctr'],dp(dist),dp(min_dist))
            if min_dist > 0 and D['ctr'] > 0:#j > 0:
                dist = np.sqrt((a[0]-a_prev[0])**2+(a[1]-a_prev[1])**2)
                if dist < min_dist:
                    cr(dp(dist),dp(min_dist))
                    continue
                else:
                    cg(dp(dist),dp(min_dist))
            c = fit3d.point_in_3D_to_point_in_2D(
                a,
                height_in_pixels = D['plot']['height_in_pixels'],
                width_in_pixels = D['plot']['width_in_pixels'],
                backup_parameter=backup_parameter,
            )
            if c[0] != False:
                D['append'](
                    na([c[0],D['plot']['height_in_pixels']-c[1]]),
                    code=code,
                    dic_info=dic_info
                )
            a_prev = a.copy()
        #cm("function_to_3D,D['ctr'] =",D['ctr'])




    D['append'] = function_append
    D['pop'] = function_pop
    D['rotate'] = function_rotate
    D['zero'] = function_zero
    D['setup_plot'] = function_setup_plot
    D['assign_plot'] = function_assign_plot
    D['show'] = function_show
    D['to_3D'] = function_to_3D
    D['check_ts'] = function_check_ts


    return D



#EOF
