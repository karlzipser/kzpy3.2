from kzpy3.utils import *
from kzpy3.misc.progress import *

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

cluster_home_path = '/global/home/users/karlz'
if home_path == cluster_home_path:
    caffe.set_mode_gpu()
    caffe.set_device(0) # select GPU device if multiple devices exist

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

def get_net(model_name):
    model_folder = model_name
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
                            mean = np.float32([114.0,114.0,114.0]),
                           #mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent
                           channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB
    print model_name

    print('reshaping data . . .')
    if model_name == 'VGG_ILSVRC_16_layers':
        net.blobs['data'].reshape(1,3,224,224)
    else:
        net.blobs['data'].reshape(1,3,227,227)
    print(np.shape(net.blobs['data'].data))
    

    for n in net.blobs.keys():
        print (np.shape(net.blobs[n].data),n)
    return net

# a couple of utility functions for converting to and from Caffe's input image layout
def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']
def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])









##########################################################
#
bvlc_reference_caffenet_layers = [
    'conv1','conv2','conv3','conv4','conv5','fc6','fc7','fc8','prob']

VGG_ILSVRC_16_layers_layers = [
    'conv1_1','conv1_2','conv2_1','conv2_2',
    'conv3_1','conv3_2','conv3_3',
    'conv4_1','conv4_2','conv4_3',
    'conv5_1','conv5_2','conv5_3',
    'fc6','fc7','fc8','prob']

bvlc_googlenet_layers = [
        'conv1/7x7_s2',
        'conv2/3x3',
        'inception_3a/1x1',
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
        'inception_5b/output',
        'prob']


##########################################################


##########################################################
#
def objective_L2(dst):
    dst.diff[:] = dst.data 

"""
def make_step(net, step_size=1.5, end='inception_4c/output', 
              jitter=32, clip=True, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    src.data[:] += step_size/np.abs(g).mean() * g

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)    
"""

def make_step2(
    net,
    step_size=1.5,
    end='', 
    jitter=5,
    clip=True,
    objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob

    dst = net.blobs[end]
    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
    net.forward(end=end)

    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    
    denom = np.abs(g).mean()
    #denom = 1.0 # 10/19/2015 temp modification
    if denom:
        src.data[:] += step_size/denom * g
    else:
        print(d2s('Warnging: denom =',denom))
        return False
    
    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)
    return True  
#
##########################################################




"""
bvlc_googlenet_person
((10, 3, 224, 224), 'data')
((10, 64, 112, 112), 'conv1/7x7_s2')
((10, 64, 56, 56), 'pool1/3x3_s2')
((10, 64, 56, 56), 'pool1/norm1')
((10, 64, 56, 56), 'conv2/3x3_reduce')
((10, 192, 56, 56), 'conv2/3x3')
((10, 192, 56, 56), 'conv2/norm2')
((10, 192, 28, 28), 'pool2/3x3_s2')
((10, 192, 28, 28), 'pool2/3x3_s2_pool2/3x3_s2_0_split_0')
((10, 192, 28, 28), 'pool2/3x3_s2_pool2/3x3_s2_0_split_1')
((10, 192, 28, 28), 'pool2/3x3_s2_pool2/3x3_s2_0_split_2')
((10, 192, 28, 28), 'pool2/3x3_s2_pool2/3x3_s2_0_split_3')
((10, 64, 28, 28), 'inception_3a/1x1')
((10, 96, 28, 28), 'inception_3a/3x3_reduce')
((10, 128, 28, 28), 'inception_3a/3x3')
((10, 16, 28, 28), 'inception_3a/5x5_reduce')
((10, 32, 28, 28), 'inception_3a/5x5')
((10, 192, 28, 28), 'inception_3a/pool')
((10, 32, 28, 28), 'inception_3a/pool_proj')
((10, 256, 28, 28), 'inception_3a/output')
((10, 256, 28, 28), 'inception_3a/output_inception_3a/output_0_split_0')
((10, 256, 28, 28), 'inception_3a/output_inception_3a/output_0_split_1')
((10, 256, 28, 28), 'inception_3a/output_inception_3a/output_0_split_2')
((10, 256, 28, 28), 'inception_3a/output_inception_3a/output_0_split_3')
((10, 128, 28, 28), 'inception_3b/1x1')
((10, 128, 28, 28), 'inception_3b/3x3_reduce')
((10, 192, 28, 28), 'inception_3b/3x3')
((10, 32, 28, 28), 'inception_3b/5x5_reduce')
((10, 96, 28, 28), 'inception_3b/5x5')
((10, 256, 28, 28), 'inception_3b/pool')
((10, 64, 28, 28), 'inception_3b/pool_proj')
((10, 480, 28, 28), 'inception_3b/output')
((10, 480, 14, 14), 'pool3/3x3_s2')
((10, 480, 14, 14), 'pool3/3x3_s2_pool3/3x3_s2_0_split_0')
((10, 480, 14, 14), 'pool3/3x3_s2_pool3/3x3_s2_0_split_1')
((10, 480, 14, 14), 'pool3/3x3_s2_pool3/3x3_s2_0_split_2')
((10, 480, 14, 14), 'pool3/3x3_s2_pool3/3x3_s2_0_split_3')
((10, 192, 14, 14), 'inception_4a/1x1')
((10, 96, 14, 14), 'inception_4a/3x3_reduce')
((10, 208, 14, 14), 'inception_4a/3x3')
((10, 16, 14, 14), 'inception_4a/5x5_reduce')
((10, 48, 14, 14), 'inception_4a/5x5')
((10, 480, 14, 14), 'inception_4a/pool')
((10, 64, 14, 14), 'inception_4a/pool_proj')
((10, 512, 14, 14), 'inception_4a/output')
((10, 512, 14, 14), 'inception_4a/output_inception_4a/output_0_split_0')
((10, 512, 14, 14), 'inception_4a/output_inception_4a/output_0_split_1')
((10, 512, 14, 14), 'inception_4a/output_inception_4a/output_0_split_2')
((10, 512, 14, 14), 'inception_4a/output_inception_4a/output_0_split_3')
((10, 160, 14, 14), 'inception_4b/1x1')
((10, 112, 14, 14), 'inception_4b/3x3_reduce')
((10, 224, 14, 14), 'inception_4b/3x3')
((10, 24, 14, 14), 'inception_4b/5x5_reduce')
((10, 64, 14, 14), 'inception_4b/5x5')
((10, 512, 14, 14), 'inception_4b/pool')
((10, 64, 14, 14), 'inception_4b/pool_proj')
((10, 512, 14, 14), 'inception_4b/output')
((10, 512, 14, 14), 'inception_4b/output_inception_4b/output_0_split_0')
((10, 512, 14, 14), 'inception_4b/output_inception_4b/output_0_split_1')
((10, 512, 14, 14), 'inception_4b/output_inception_4b/output_0_split_2')
((10, 512, 14, 14), 'inception_4b/output_inception_4b/output_0_split_3')
((10, 128, 14, 14), 'inception_4c/1x1')
((10, 128, 14, 14), 'inception_4c/3x3_reduce')
((10, 256, 14, 14), 'inception_4c/3x3')
((10, 24, 14, 14), 'inception_4c/5x5_reduce')
((10, 64, 14, 14), 'inception_4c/5x5')
((10, 512, 14, 14), 'inception_4c/pool')
((10, 64, 14, 14), 'inception_4c/pool_proj')
((10, 512, 14, 14), 'inception_4c/output')
((10, 512, 14, 14), 'inception_4c/output_inception_4c/output_0_split_0')
((10, 512, 14, 14), 'inception_4c/output_inception_4c/output_0_split_1')
((10, 512, 14, 14), 'inception_4c/output_inception_4c/output_0_split_2')
((10, 512, 14, 14), 'inception_4c/output_inception_4c/output_0_split_3')
((10, 112, 14, 14), 'inception_4d/1x1')
((10, 144, 14, 14), 'inception_4d/3x3_reduce')
((10, 288, 14, 14), 'inception_4d/3x3')
((10, 32, 14, 14), 'inception_4d/5x5_reduce')
((10, 64, 14, 14), 'inception_4d/5x5')
((10, 512, 14, 14), 'inception_4d/pool')
((10, 64, 14, 14), 'inception_4d/pool_proj')
((10, 528, 14, 14), 'inception_4d/output')
((10, 528, 14, 14), 'inception_4d/output_inception_4d/output_0_split_0')
((10, 528, 14, 14), 'inception_4d/output_inception_4d/output_0_split_1')
((10, 528, 14, 14), 'inception_4d/output_inception_4d/output_0_split_2')
((10, 528, 14, 14), 'inception_4d/output_inception_4d/output_0_split_3')
((10, 256, 14, 14), 'inception_4e/1x1')
((10, 160, 14, 14), 'inception_4e/3x3_reduce')
((10, 320, 14, 14), 'inception_4e/3x3')
((10, 32, 14, 14), 'inception_4e/5x5_reduce')
((10, 128, 14, 14), 'inception_4e/5x5')
((10, 528, 14, 14), 'inception_4e/pool')
((10, 128, 14, 14), 'inception_4e/pool_proj')
((10, 832, 14, 14), 'inception_4e/output')
((10, 832, 7, 7), 'pool4/3x3_s2')
((10, 832, 7, 7), 'pool4/3x3_s2_pool4/3x3_s2_0_split_0')
((10, 832, 7, 7), 'pool4/3x3_s2_pool4/3x3_s2_0_split_1')
((10, 832, 7, 7), 'pool4/3x3_s2_pool4/3x3_s2_0_split_2')
((10, 832, 7, 7), 'pool4/3x3_s2_pool4/3x3_s2_0_split_3')
((10, 256, 7, 7), 'inception_5a/1x1')
((10, 160, 7, 7), 'inception_5a/3x3_reduce')
((10, 320, 7, 7), 'inception_5a/3x3')
((10, 32, 7, 7), 'inception_5a/5x5_reduce')
((10, 128, 7, 7), 'inception_5a/5x5')
((10, 832, 7, 7), 'inception_5a/pool')
((10, 128, 7, 7), 'inception_5a/pool_proj')
((10, 832, 7, 7), 'inception_5a/output')
((10, 832, 7, 7), 'inception_5a/output_inception_5a/output_0_split_0')
((10, 832, 7, 7), 'inception_5a/output_inception_5a/output_0_split_1')
((10, 832, 7, 7), 'inception_5a/output_inception_5a/output_0_split_2')
((10, 832, 7, 7), 'inception_5a/output_inception_5a/output_0_split_3')
((10, 384, 7, 7), 'inception_5b/1x1')
((10, 192, 7, 7), 'inception_5b/3x3_reduce')
((10, 384, 7, 7), 'inception_5b/3x3')
((10, 48, 7, 7), 'inception_5b/5x5_reduce')
((10, 128, 7, 7), 'inception_5b/5x5')
((10, 832, 7, 7), 'inception_5b/pool')
((10, 128, 7, 7), 'inception_5b/pool_proj')
((10, 1024, 7, 7), 'inception_5b/output')
((10, 1024, 1, 1), 'pool5/7x7_s1')
((10, 1000), 'loss3/classifier')
((10, 1000), 'prob')

"""


