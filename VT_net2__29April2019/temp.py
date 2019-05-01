
def Array(max_len,n_dims):#,n_code_dims=0):
    D = {}
    D['max_len'] = max_len
    D['n_dims'] = n_dims
    #D['n_code_dims'] = n_code_dims
    D['data'] = zeros((2*max_len,n_dims+1+1))#+n_code_dims))
    D['array'] = D['data'][:,:n_dims]
    D['keys'] = D['data'][:,-1]
    D['code'] = D['data'][:,n_dims]#:n_dims+n_code_dims]
    D['ctr'] = 0
    D['key_ctr'] = 0
    D['Dic'] = {}

    def function_check_len():
        ctr = D['ctr']
        max_len = D['max_len']
        cm(max_len,ctr-max_len,ctr)
        if ctr > 1.5*max_len:
            cm(max_len,ctr-max_len,ctr)
            D['data'][:max_len,:] = D['data'][ctr-max_len:ctr,:]
            D['data'][-max_len:,:] = 0
            D['ctr'] = max_len
            cy(ctr)
            kys = list(D['keys'])
            for k in D['Dic'].keys():
                if k not in kys:
                    del D['Dic'][k]

    #zero_code_array = zeros(n_code_dims)

    def function_append(a,code,dic_info=None):#,code_array=zero_code_array,dic_info=None):
        function_check_len()
        ctr = D['ctr']
        D['array'][ctr,:] = a
        D['keys'][ctr] = D['key_ctr']
        D['code'][ctr] = code #code_array
        D['Dic'][D['key_ctr']] = dic_info
        D['ctr'] += 1
        D['key_ctr'] += 1

    def function_rotate(deg):
        rotatePolygon__array_version(D['array'],deg)

    def function_zero():
        D['array'][:D['ctr'],:] -= D['array'][D['ctr']-1] #path_pts2D[-1]

    D['append'] = function_append
    D['rotate'] = function_rotate
    D['zero'] = function_zero

    return D

if False:
    A = Array(7,2)#,2) 
    for i in range(50):
        A['append'](na([i,i]),np.random.randint(4),i*i)
        A['rotate'](1.)
        A['zero']()
        cg(A['data'],ra=1)