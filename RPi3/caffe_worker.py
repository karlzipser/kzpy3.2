import caffe
from kzpy3.utils import *

# rsync -avz ~/Desktop/RPi3_data/runs_scale_50_BW/ kzipser@redwood2.dyn.berkeley.edu:'~/Desktop/runs_scale_50_BW'

os.chdir(home_path) # this is for the sake of the train_val.prototxt
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px.prototxt"))
#solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_11px_MC.prototxt"))

#solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_scl50_steer_only/original_with_accuracy_11px_scl50_iter_1200000.caffemodel'))
#solver.net.copy_from(opjh('scratch/2016/3/RPi3/11px_MC_rw2/11px_MC_iter_6800000.caffemodel'))
solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_11100000.caffemodel'))
for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
    print(l)
for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
    print(l)


while True:
    try:
        solver.net.forward();
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    try:
        steer = solver.net.blobs['ip2'].data[0][0]
        steer -= 0.5
        steer *= 100
        steer = int(steer)

        np.save(opjh('Desktop/caffe_command.npy'),steer)
        print (steer,int(100*(solver.net.blobs['ip2'].data[0][1])),int(100*(solver.net.blobs['ip2'].data[0][2])))
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))



