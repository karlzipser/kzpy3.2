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



clusters = loD('cluster_list_25_1st_pass.pkl')

indicies = []
c = []
for i in range(1024):
    for j in range(len(clusters[i])):
        indicies.append(clusters[i][j]['index'])
#EOF