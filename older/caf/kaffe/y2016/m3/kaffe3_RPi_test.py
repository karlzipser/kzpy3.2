"""
python kzpy3/caf/kaffe/y2016/m3/kaffe3_new_start.py
"""

from kzpy3.vis import *
from kzpy3.misc.progress import *
from google.protobuf import text_format
import caffe

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet',
'finetune_BarryLyndon_8Sept2015','VGG_ILSVRC_16_layers','person_clothing_bigger_18Sept2015',
'bvlc_googlenet_person']

def get_net(MODEL_NUM = 2):
    model_folder = model_folders[MODEL_NUM]
    model_path = opj(home_path,'caffe/models',model_folder)
    net_fn   = opj(model_path,'deploy.prototxt')
    param_fn = opj(model_path,'model.caffemodel')
    # Patching model to be able to compute gradients.
    # Note that you can also manually add "force_backward: true" line to "deploy.prototxt".
    model = caffe.io.caffe_pb2.NetParameter()
    text_format.Merge(open(net_fn).read(), model)
    model.force_backward = True
    open('tmp.prototxt', 'w').write(str(model))
    net = caffe.Classifier('tmp.prototxt', param_fn,
                           mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent
                           channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB
    print model_folders[MODEL_NUM]
    for n in net.blobs.keys():
        print (np.shape(net.blobs[n].data),n)
    return net


# a couple of utility functions for converting to and from Caffe's input image layout
def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['py_image_data']
def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['py_image_data'])[::-1])



def objective_L2(dst):
    dst.diff[:] = dst.data 


def make_step(net, step_size=1.5, end='inception_4c/output', 
              jitter=0, clip=False, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = net.blobs['py_image_data'] # input image is stored in Net's 'py_image_data' blob
    dst = net.blobs[end]

    #ox, oy = np.random.randint(-jitter, jitter+1, 2)
    #src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(start='py_image_data',end=end)
    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    src.data[:] += step_size/np.abs(g).mean() * g

    #src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
 

def show_py_image_data(net):
    for i in range(9): 
        mi(net.blobs['py_image_data'].data[0,i,:,:])
        plt.pause(0.2)


def do_it3(dst_path,layer,net,iter_n,start=0):


    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,dst_path,model_folders[MODEL_NUM]+'/'+layer.replace('/','-'))
    unix('mkdir -p ' + img_path)
    for n in [start]:#n in range(start,layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7

        for i in range(9):
            net.blobs['py_image_data'].data[0][i,:,:] = np.random.random(np.shape(net.blobs['py_image_data'].data[0][1,:,:]))-0.5


        pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['py_image_data']
            #vis = deprocess(net, src.data[0])
            if np.mod(i,10.0)==0:
                pb.animate(i+1)
        print((model_folders[MODEL_NUM],layer,n))
        #vis = deprocess(net, src.data[0])
        #print shape(vis)
        np.save(opj(img_path,str(n)+'.npy'),src.data[0])

        net.blobs['py_image_data'].data[0,:,0,0]=net.blobs['py_image_data'].data[:].max()
        net.blobs['py_image_data'].data[0,:,0,1]=net.blobs['py_image_data'].data[:].min()

        show_py_image_data(net)

inception_layers = ['inception_3a/1x1',
        'inception_3a/3x3',
        'inception_3a/5x5',
        'inception_3a/output',
        'inception_3b/1x1',
        'inception_3b/3x3',
        'inception_3b/5x5',
        'inception_3b/output',
        'inception_4a/1x1',
        'inception_4a/3x3',
        'inception_4a/5x5',
        'inception_4a/output',
        'inception_4b/1x1',
        'inception_4b/3x3',
        'inception_4b/5x5',
        'inception_4c/1x1',
        'inception_4c/3x3',
        'inception_4c/5x5',
        'inception_4c/output',
        'inception_4d/1x1',
        'inception_4d/3x3',
        'inception_4d/5x5',
        'inception_4d/output',
        'inception_4e/1x1',
        'inception_4e/3x3',
        'inception_4e/5x5',
        'inception_4e/output',
        'inception_5a/1x1',
        'inception_5a/3x3',
        'inception_5a/5x5',
        'inception_5a/output',
        'inception_5b/1x1',
        'inception_5b/3x3',
        'inception_5b/5x5',
        'inception_5b/output']






MODEL_NUM = 5
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_kaffe_11px.prototxt"))
#solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_11100000.caffemodel'))
net = solver.net

"""
for i in net.params.keys():
    net.params[i][0].data[0] = np.random.random(shape(net.params[i][0].data[0]))

print(np.shape(net.blobs['py_image_data'].data))
src = net.blobs['py_image_data']
#src.reshape(1,3,227,227)
print(np.shape(net.blobs['py_image_data'].data))

for i in range(96):
    print i
    for l in ['ip1']:#['inception_4e/output']:#['fc8']:
        do_it3('scratch/2016/3/6',l,net,1000,i)
    time.sleep(1)
    show_py_image_data(net)
"""

