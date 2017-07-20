

files = sgg('/home/karlzipser/Desktop/bair_car_data_Main_Dataset/hdf5/runs/*.hdf5')



Fp={}
Sp={}
for path in files:
	try:
		#for path in files[0]:
		Fp[path] = h5py.File(path)
		Sp[path] = F[path]['segments']
	except:
		print 'oops'

ctr = 0
T = 10.0
timer = Timer(T)

while not timer.check():
	try:
		i = random.randint(0,len(files)-1)
		f = files[i]
		S = Sp[f]
		Sk = S.keys()
		i = random.randint(0,len(Sk)-1)
		s = S[Sk[i]]
		r = s['right'][random.randint(0,len(s['right'])-1),:,:,:]
		#mci(r)
		ctr += 1
	except:
		print 'woops'
		print ctr
pd2s(ctr/T,'Hz')
