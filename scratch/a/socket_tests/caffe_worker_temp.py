import caffe
#!/usr/bin/python

import thread
import time

# Define a function for the thread
def print_time2( threadName, delay):
    count = 0
    while count < delay:
        time.sleep(0.1)
        count += 1
        print "---------->%s: %s" % ( threadName, time.ctime(time.time()) )
    print "Done with " + threadName

from kzpy3.utils import *

os.chdir(home_path) # this is for the sake of the train_val.prototxt
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_no_py_layers.prototxt"))
solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_11100000.caffemodel'))

for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
    print(l)
for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
    print(l)






def get_caffe_input_target():
    img_lst = []
    for i in range(9):
        dummy = np.random.random((56,75))
        img_lst.append(dummy)
    return img_lst



def print_time1( threadName, delay):
    count = 0
    while count < delay:
        count += 1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )
        try:
            img_lst = get_caffe_input_target()
            for i in range(len(img_lst)):
                solver.net.blobs['py_image_data'].data[0,i,:,:] = img_lst[i]
            solver.net.forward();
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
        try:
            steer = solver.net.blobs['ip2'].data[0][0]
            steer -= 0.5
            steer *= 100
            steer = int(steer)
            print steer
            #print (steer,int(100*(solver.net.blobs['ip2'].data[0][1])),int(100*(solver.net.blobs['ip2'].data[0][2])))
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e))
    print "Done with " + threadName




# Create two threads as follows
try:
   thread.start_new_thread( print_time1, ("caffe thread-1", 100, ) )
   thread.start_new_thread( print_time2, ("Thread-2", 100, ) )
except:
   print "Error: unable to start thread"





