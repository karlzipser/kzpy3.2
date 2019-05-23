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

    def function_rotate(deg):
        rotatePolygon__array_version(D['array'],deg)

    def function_zero():
        D['array'][:D['ctr'],:] -= D['array'][D['ctr']-1]

    def function_test_Array():
        A = Array(7,2)
        for i in range(50):
            A['append'](na([i,i]),np.random.randint(4),i*i)
            A['rotate'](1.)
            A['zero']()
            for j in rlen(A['array']):
                a = A['data'][j,:] 
                cg(int(a[2]),yl,(intr(a[0]),intr(a[1])),bl,int(a[3]),sf=0)
            raw_enter()

    D['append'] = function_append
    D['rotate'] = function_rotate
    D['zero'] = function_zero
    D['test'] = function_test_Array

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
