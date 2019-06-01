from kzpy3.vis3 import *

import kzpy3.misc.fit3d as fit3d










            

##############################################################
##############################################################
###
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
        use_maplotlib=True,
        do_print=True,
        clear=True,
        color=(255,255,255),
        code=None,
        show=True,
        grid=True,
        scale=1.0,
    ):
        if code == None:
            the_array = D['array']
        else:
            the_array = D['array'][D['code']==code]


        if clear:
            D['plot']['clear']()
        if grid:
            D['plot']['grid']()
        if do_print:
            for j in rlen(D['array']):
                a = D['data'][j,:] 
                cg(int(a[2]),yl,(intr(a[0]),intr(a[1])),bl,int(a[3]),sf=0)
        if use_CV2_plot:
            D['plot']['pts_plot'](the_array,c=color)
            if show:
                D['plot']['show'](title=D['name'],scale=scale)
        if use_maplotlib:
            if clear:
                clf()
            pts_plot(the_array,color=rndchoice(['r','g','k','b','m','c']))
            if show:
                #xysqlim(10)
                plt_square()
                spause()

    D['append'] = function_append
    D['rotate'] = function_rotate
    D['zero'] = function_zero
    D['setup_plot'] = function_setup_plot
    D['show'] = function_show
    return D


###
##############################################################
##############################################################





def _test_Array(test_num=1):
    
    CA()
    height_in_pixels = 200
    width_in_pixels = 200

    if test_num == 1:
        img = zeros((94,168))
        n = 20*20*10
        A = Array(n,2)
        A['setup_plot'](
            height_in_pixels=200,
            width_in_pixels=200,
            pixels_per_unit=10,
            x_origin_in_pixels=None,
            y_origin_in_pixels=None,
        )
        """
        for i in range(n):
            a = 20*rndn(2)
            if True:#a[1] > -1000:
                if True:#a[0] > 0:
                    A['append'](a)
            #A['rotate'](3.)
            #A['zero']()
        """
        for x in arange(-10,10,2):
            for y in arange(-10,10,.1):
                A['append'](na([x,y]))

        A['show'](
            do_print=False,
            use_maplotlib=False
        )
        
        clf();plt_square()
        for j in range(A['max_len']):
            a = A['array'][j,:]

            c = point_in_3D_to_point_in_2D(a)
            if c[0] != False:
                cy(a,int(c[0]),int(c[1]))
                #plot(c[0],c[1],'r.');spause()
                img[int(c[1]),int(c[0])]=1/(np.sqrt(a[0]**2+a[1]**2))
        mi(img)
        #raw_enter()
        
    elif test_num == 2:
        height_in_pixels = 200
        width_in_pixels = 200
        A = Array(500,2)
        for i in range(500):
            r = rndn(2)
            if r[0] >= 0 and r[1] >= 0:
                c = 1
            elif r[0] <= 0 and r[1] <= 0:
                c = 2
            else:
                c = 0
            A['append'](r,code=c)
        A['show'](
            height_in_pixels=height_in_pixels,
            width_in_pixels=width_in_pixels,
            pixels_per_unit=30,
            do_print=False,
            use_maplotlib=False,
            color=(255,0,0),
            code=1,
            show=False
        )
        A['show'](
            do_print=False,
            use_maplotlib=False,
            color=(0,0,255),
            code=2,
            clear=False,
            show=False,
        )
        A['show'](
            do_print=False,
            use_maplotlib=False,
            color=(0,255,0),
            code=0,
            clear=False
        )
        raw_enter()




def test_Array(test_num=1):


    img = zeros((94,168))
    n = 20*20*10
    A = Array(n,2)
    B = Array(n,2)

    A['setup_plot'](
        height_in_pixels=500,
        width_in_pixels=500,
        pixels_per_unit=50,
    )
    B['setup_plot'](
        height_in_pixels=94,
        width_in_pixels=168,
        x_origin_in_pixels=0,
        y_origin_in_pixels=94,
        pixels_per_unit=1,
    )
    

    for x in arange(-0.0,10,1):
        for y in arange(0,10,.1):
            A['append'](na([x,y]))
    for x in arange(-10,0,.1):
        for y in arange(0,10,1):
            A['append'](na([x,y]))

    for j in range(A['ctr']):
        a = A['array'][j,:]

        c = point_in_3D_to_point_in_2D(a)
        if c[0] != False:
            #cy(a,int(c[0]),int(c[1]))
            B['append'](na([c[0],94-c[1]]))
            #img[int(c[1]),int(c[0])]=1/(np.sqrt(a[0]**2+a[1]**2))

    A['show'](
        do_print=False,
        use_maplotlib=False,
    )

    B['show'](
        do_print=False,
        use_maplotlib=False,
        grid=False,
        scale=3.0,
    )
    #mi(B['plot']['image'])
    
    



def point_in_3D_to_point_in_2D(a,backup_parameter=1.0):
    if a[1]<0:
        return False,False

    b = fit3d.Point3(a[0], 0, a[1] - backup_parameter)
    c = fit3d.project(b, fit3d.mat)

    if c.x < 0 or c.x >= 168:
        return False,False

    elif c.y < 0 or c.y >= 94:
        return False,False

    return c.x,c.y


if __name__ == '__main__':
    test_Array()
    raw_enter()

#EOF
