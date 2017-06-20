from kzpy3.vis import *
import caffe
from kzpy3.utils import *
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



MODEL_NUM = 2
net = get_net(MODEL_NUM)


#solver = caffe.SGDSolver("/Users/karlzipser/Google_Drive/models_caffe/bvlc_alexnet/solver.prototxt")
#f=opjD('/Users/karlzipser/Google_Drive/models_caffe/bvlc_alexnet/bvlc_alexnet.caffemodel')
#solver.net.copy_from(f)


def mi_data(data,fig):
	d = zeros((shape(data)[2],shape(data)[3],3))
	d[:,:,0] = data[0,2,:,:]
	d[:,:,1] = data[0,1,:,:]
	d[:,:,2] = data[0,0,:,:]
	d = z2o(d)
	mi(d,fig)

step_size = 1.5#0.333
jitter = 0
src = net.blobs['data']
src.data[0] = 0*src.data[0]
for j in range(1000):

	ox, oy = np.random.randint(-jitter, jitter+1, 2)
	src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift

	net.forward()
	print(net.blobs['fc8'].data[0,:4])
	net.blobs['fc8'].diff[0] *= 0
	net.blobs['fc8'].diff[0,3]=1
#	solver.net.blobs['conv1'].diff[0] *= 0
#	solver.net.blobs['conv1'].diff[0,30,8,15] = 1
#	net.blobs['conv1'].diff[0,2,15,8] = 1
	net.backward(start='fc8')
#	net.backward(start='conv1')
	g = src.diff[0]
	src.data[:] += step_size/np.abs(g).mean() * g
	src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image

