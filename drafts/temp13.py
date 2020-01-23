def setup(P):

    Runs = {}

    #activation_folders = sggo(opjm('2_TB_Samsung','Activations_folders','*'))
    activation_folders = sggo(opjD('Data', 'Activations_folders','*'))
    
 



N = h5r('/home/karlzipser/Desktop/Data/Network_Predictions_projected/Mr_Black_01Oct18_18h58m41s.net_projections.h5py')


d = N['normal']


def norm_by_sum(a):
	for i in range(3):
		a = a.astype(float)
		#a[:,:,i] /= (a[:,:,i].astype(float).sum()*1.0)
	return a


def similarity(a,b):
	aa = norm_by_sum(a)
	bb = norm_by_sum(b)
	s = 0
	for i in range(3):
		dd = ((aa-bb)**2).sum()
		s += ((aa-bb)**2).sum()
	return s


a = d[rndint(len(d))]
b = d[rndint(len(d))]
a[0,0,:] = (255,0,0)
a[1,0,:] = (0,1,0)
a[2,0,:] = (0,0,1)


mi(a,'a')
mi(b,'b')
print similarity(a,b)


