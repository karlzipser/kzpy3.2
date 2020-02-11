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

oo(D,5,2,3,eq=5)

kprint(D,'\nD')

c(D,10,v={1:2})

kprint(D,'\nD')

c(D,10,2,v=0.0)
c(D,10,3,v=0.0)
c(D,10,4,v=0.0)

kprint(D,'\nD')


oo(X, 2, 3, oo(D, 0), eq= oo(D, 5) )

apple_ = 'apple'
bear_ = 'bear'

a = D[0]['apple']['bear']['c']

a = D[0][apple_][bear_][c_]


a = oo(D,0,apple_,bear_,c_)

b = D[5]
oo(X, 2, 3, a, eq= b)

#,b

#EOF
