from kzpy3.vis3 import *
exec(identify_file_str)

n = 32

m = zeros((3*n,3*n))

ctr = 0
for x in range(n):
    for y in range(n):
        m[n+x,n+y] = ctr
        m[x,n+y] = ctr
        m[2*n+x,n+y] = ctr
        m[n+x,y] = ctr
        ctr += 1

mi(m)


#EOF