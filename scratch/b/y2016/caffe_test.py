
import caffe
from kzpy3.utils import *

solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_scl50_nin.prototxt"))

for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
	print(l)
for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
	print(l)
return solver


solver = setup_solver()
solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_scl50_nin/original_with_accuracy_11px_scl50_nin_iter_300000.caffemodel'))

