
# # Instant Recognition with Caffe
# (These feature visualizations follow the DeCAF visualizations originally by Yangqing Jia.)


from kzpy3.vis import *

# Make sure that caffe is on the python path:
caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

caffe.set_mode_cpu()
net = caffe.Net(opj(caffe_root,'models/bvlc_reference_caffenet/deploy.prototxt'),
                opj(caffe_root, 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'),
                caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(opj(caffe_root,'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB


net.blobs['data'].reshape(1,3,227,227)

#f = opj(caffe_root,'examples/images/cat.jpg')
f = opjD('RPi3_data/runs_scl_100_RGB/09Feb16_13h33m51s_scl=100_mir=0/310_1455053662.01_str=0_spd=66_rps=29_lrn=55_rrn=67_rnd=0_scl=100_mir=0_.jpg')

net.blobs['data'].data[...] = transformer.preprocess('data', caffe.io.load_image(f)) #caffe.io.load_image(caffe_root + 'examples/images/cat.jpg'))
out = net.forward()
print("Predicted class is #{}.".format(out['prob'].argmax()))


# What did the input look like?


mi(transformer.deprocess('data', net.blobs['data'].data[0]),1)


# Adorable, but was our classification correct?

# In[8]:

# load labels
imagenet_labels_filename = opj(caffe_root,'data/ilsvrc12/synset_words.txt')
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    get_ipython().system('../data/ilsvrc12/get_ilsvrc_aux.sh')
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

# sort top k predictions from softmax output
top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
print labels[top_k]


# Indeed! But how long did it take?

# In[9]:

# CPU mode
net.forward()  # call once for allocation
get_ipython().magic('timeit net.forward()')


# First, the layer features and their shapes (1 is the batch size, corresponding to the single input image in this example).

# In[25]:

[(k, v.data.shape) for k, v in net.blobs.items()]


# The parameters and their shapes. The parameters are `net.params['name'][0]` while biases are `net.params['name'][1]`.

# In[26]:

[(k, v[0].data.shape) for k, v in net.params.items()]


# Helper functions for visualization

# In[27]:

# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0, fig=10):
    data -= data.min()
    data /= data.max()
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    mi(data,fig)


# The input image

# The first layer filters, `conv1`

# In[28]:

# the parameters are a list of [weights, biases]

def show_conv_feat(net):
    filters = net.params['conv1'][0].data
    vis_square(filters.transpose(0, 2, 3, 1),fig='conv1')
    feat = net.blobs['conv1'].data[0, :]
    vis_square(feat, padval=1,fig='conv1 feat')
    filters = net.params['conv2'][0].data
    vis_square(filters[:48].reshape(48**2, 5, 5),fig='conv2')
    feat = net.blobs['conv2'].data[0, :]
    vis_square(feat, padval=1,fig='conv2 feat')
    feat = net.blobs['conv3'].data[0]
    vis_square(feat, padval=0.5,fig='conv3 feat')
    feat = net.blobs['conv4'].data[0]
    vis_square(feat, padval=0.5,fig='conv4 feat')
    feat = net.blobs['conv5'].data[0]
    vis_square(feat, padval=0.5,fig='conv5 feat')
    feat = net.blobs['pool5'].data[0]
    vis_square(feat, padval=1,fig='pool5 feat')


# The first fully connected layer, `fc6` (rectified)
# 
# We show the output values and the histogram of the positive values

# In[36]:

feat = net.blobs['fc6'].data[0]
plt.subplot(2, 1, 1)
plt.plot(feat.flat)
plt.subplot(2, 1, 2)
_ = plt.hist(feat.flat[feat.flat > 0], bins=100)


# The second fully connected layer, `fc7` (rectified)

# In[37]:

feat = net.blobs['fc7'].data[0]
plt.subplot(2, 1, 1)
plt.plot(feat.flat)
plt.subplot(2, 1, 2)
_ = plt.hist(feat.flat[feat.flat > 0], bins=100)


# The final probability output, `prob`

# In[38]:

feat = net.blobs['prob'].data[0]
plt.plot(feat.flat)


# Let's see the top 5 predicted labels.

# In[39]:

# load labels
imagenet_labels_filename = opj(caffe_root,'data/ilsvrc12/synset_words.txt')
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    get_ipython().system('../data/ilsvrc12/get_ilsvrc_aux.sh')
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')

# sort top k predictions from softmax output
top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
print labels[top_k]

