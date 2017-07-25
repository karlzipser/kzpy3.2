o=lo('/media/karlzipser/ExtraDrive2/bair_car_data_Main_Dataset/rgb_1to4/direct_local_01Jan17_14h59m21s_Mr_Black/bair_car_2017-01-01-15-33-31_58.bag.pkl')
r=o['right']
k=sorted(r.keys())

for i in range(0,870):
	q=r[k[i]]
	w=r[k[i+1]]
	mi(q[:,:,0]*1.0-w[:,:,0]*1.0,1,[1,1,1]);mi(q,2)
	pause(0.01)



l,s=function_load_hdf5(p)
for j in rlen(s):
	a=s[str(j)]
	l=a['left']
	r=a['right']
	for i in range(shape(l)[0]-1):
		L = l[i+1,:,:,1]*1.0-l[i,:,:,1]*1.0
		R = r[i+1,:,:,1]*1.0-r[i,:,:,1]*1.0
		mi(L-R,1)
		mi(l[i,:,:,1],2)
		pause(0.001)


