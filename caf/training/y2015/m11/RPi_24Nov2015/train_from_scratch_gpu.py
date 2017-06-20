from kzpy3.utils import *
#sys.path.insert(0, './python')
import caffe


"""
cms = gg(opjh('caffe/models/person_clothing_17Sept2015/*.caffemodel'))
ctimes = []
for c in cms:
    ctimes.append(os.path.getctime(c))
cms = sorted(cms,key=natural_keys)
ctimes = []
for c in cms:
    ctimes.append(os.path.getctime(c))
sorted_indicies = np.argsort(np.array(ctimes))
model_to_load = cms[sorted_indicies[-1]]
print(d2s('***** model to load =',model_to_load))
"""



#caffe.set_device(0)
caffe.set_mode_cpu()
solver = caffe.SGDSolver(opjh('kzpy3/caf/training/y2015/m11/RPi_24Nov2015/solver_gpu.prototxt'))
"""
solver.net.copy_from(model_to_load)
"""

niter = 500000
train_loss = []
accuracy_lst = []



for it in range(niter):
    try:
        solver.step(1)  # SGD by Caffe
    except:
        pass
print 'done'



