#,a

file_path = opjD('temp.h5py')

D = {}

for k in ['a','b','c']:
	D[k] = []
	for i in range(10):
		D[k].append(rndn(32,20,10))

def save_as_h5py(file_path,D,dtype='float16'):
	F = h5w(file_path)
	clp('topics:')
	for k in D.keys():
		D[k] = na(D[k])
		clp('\t',k,len(D[k]))
		F.create_dataset(k,data=D[k],dtype=dtype)	
	F.close()

F = h5r(file_path)
for k in F.keys():
	d = F[k][0,0,:,:].astype(float)
	mi(d,k)
F.close()

#,b



