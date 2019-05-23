from kzpy3.vis3 import *



def Array(max_len,n_dims):
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
    D['CV2Plot'] = None

    def function_check_len():
        ctr = D['ctr']
        max_len = D['max_len']
        if ctr > 1.5*max_len:
            #cm(max_len,ctr-max_len,ctr)
            D['data'][:max_len,:] = D['data'][ctr-max_len:ctr,:]
            D['data'][-max_len:,:] = 0
            D['ctr'] = max_len
            kys = list(D['keys'])
            for k in D['Dic'].keys():
                if k not in kys:
                    del D['Dic'][k]

    def function_append(a,code,dic_info=None):
        function_check_len()
        ctr = D['ctr']
        D['array'][ctr,:] = a
        D['keys'][ctr] = D['key_ctr']
        D['code'][ctr] = code
        if dic_info != None:
            D['Dic'][D['key_ctr']] = dic_info
        D['ctr'] += 1
        D['key_ctr'] += 1
        D['C'] = None
    def function_rotate(deg):
        rotatePolygon__array_version(D['array'],deg)

    def function_zero():
        D['array'][:D['ctr'],:] -= D['array'][D['ctr']-1]

    def function_test_Array():
        A = Array(30,2)
        CA()
        height_in_pixels = 200
        width_in_pixels = 200
        for i in range(50):
            A['append'](na([0,1]),np.random.randint(4),i*i)
            A['rotate'](3.)
            A['zero']()
            A['show'](
                height_in_pixels=height_in_pixels,
                width_in_pixels=width_in_pixels,
                x_origin_in_pixels=0,
                y_origin_in_pixels=0,
                do_print=False,
                use_maplotlib=False
            )
            #height_in_pixels+=3*i
            #width_in_pixels+=3*i
            raw_enter()

    def function_show(
        height_in_pixels=200,
        width_in_pixels=200,
        pixels_per_unit=3,
        x_origin_in_pixels=None,
        y_origin_in_pixels=None,
        use_CV2_plot=True,
        use_maplotlib=True,
        do_print=True,
        clear=True):
        if D['CV2Plot'] == None:
            D['CV2Plot'] = CV2Plot(
                height_in_pixels,
                width_in_pixels,
                pixels_per_unit,
                x_origin_in_pixels,
                y_origin_in_pixels
            )
        if clear:
            D['CV2Plot']['clear']()
        if do_print:
            for j in rlen(D['array']):
                a = D['data'][j,:] 
                cg(int(a[2]),yl,(intr(a[0]),intr(a[1])),bl,int(a[3]),sf=0)
        if use_CV2_plot:
            D['CV2Plot']['pts_plot'](D['array'])
            D['CV2Plot']['show']()
        if use_maplotlib:
            clf()
            pts_plot(D['array'])
            xysqlim(30)
            plt_square()
            spause()


    D['append'] = function_append
    D['rotate'] = function_rotate
    D['zero'] = function_zero
    D['test'] = function_test_Array
    D['show'] = function_show
    return D



##############################################################
###
def get__path_pts2D(
    d_heading,
    encoder,
    sample_frequency,
    direction,
    value,
    Path_pts2D,
    _
):

    velocity = encoder * _['vel-encoding coeficient'] * direction

    trajectory_vector = na([0,1]) * velocity / sample_frequency

    try:
        Path_pts2D['rotate'](-d_heading * sample_frequency * _['d_heading_multiplier'])
    except:
        pass

    Path_pts2D['append'](trajectory_vector,value,{'velocity':velocity})

    Path_pts2D['zero']()

###
##############################################################



#EOF
