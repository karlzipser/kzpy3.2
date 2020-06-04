


def dist(A,B):
    return np.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )

def distance_decimate_vector(v,d):
    ref = v[0,:]
    u = [ref]
    for i in range(0,len(v)-1):
        e = dist(v[i],v[i+1])
        if dist(ref,v[i]) >= d:
        	ref = v[i]
        	u.append(ref)
    u.append(v[-1])
    return na(u)



