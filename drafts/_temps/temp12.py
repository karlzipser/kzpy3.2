#,a

def c(D,*args,**kwargs):
    assert type(D) == dict
    assert len(args) > 0
    a = args[0]
    
    if a not in D:
        if  'v' in kwargs:
            clp(host_name+':','warning, adding',a,'to dic','`--r')
            D[a] = {}

    if len(args) == 1:

        if 'v' in kwargs:
            D[a] = kwargs['v']

        return D[a]

    else:

        assert len(args) > 1

        if 'v' in kwargs:
            return c(D[a],*args[1:],v=kwargs['v'])

        else:
            return c(D[a],*args[1:])



D = {0:2,1:{2:{3:4}},5:{2:{3:9}}}
kprint(D,'\nD')

c(D,5,2,3,v=5)

kprint(D,'\nD')

c(D,10,v={1:2})

kprint(D,'\nD')

c(D,10,2,v=0.0)
c(D,10,3,v=0.0)
c(D,10,4,v=0.0)

kprint(D,'\nD')


c(X, 2, 3, c(D, 0), v=c(D, 5) )

#,b

#EOF
