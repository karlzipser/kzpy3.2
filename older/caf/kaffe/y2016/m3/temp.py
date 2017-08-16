from kzpy3.utils import *
def temp(solver):
	n=1000
	results = np.zeros((7,7))
	ctrs = np.zeros(7)
	for i in range(n):
		solver.net.forward()
		j = solver.net.blobs['py_target_data'].data[0].argmax(axis=0)
		results[j,:] += solver.net.blobs['ip3'].data[0]
		ctrs[j] += 1.0
	for i in range(7):
		results[i,:] /= ctrs[i]
	print results
