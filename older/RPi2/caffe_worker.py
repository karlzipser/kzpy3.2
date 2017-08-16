from kzpy3.utils import *
import caffe

os.chdir(home_path) # this is for the sake of the train_val.prototxt
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m1/from_mnist/original_with_accuracy/solver_deploy.prototxt"))
solver.net.copy_from(opjD('model_iter_400000.caffemodel'))

img_path = opjh('scratch/2015/11/RPi_images/')

while True:
    print time.time()
    try:
        solver.net.forward() 
        #print solver.net.blobs['ip2'].data
        recent = solver.net.blobs['ip2'].data[0][:9].mean()
        predicted = solver.net.blobs['ip2'].data[0][9:].mean()
        print(recent,predicted)
        np.save(opjD('net_command.npy'),(recent,predicted))
    except:
        print "solver failed"
    time.sleep(0.333)
