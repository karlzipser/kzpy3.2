from kzpy3.utils import *
from kzpy3.progress import *
#plt.ion()

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

# caffe.set_mode_gpu()
# caffe.set_device(0) # select GPU device if multiple devices exist

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet','finetune_BarryLyndon_8Sept2015']

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
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']
def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])


imagenet_labels_filename = opj(home_path,'caffe/data/ilsvrc12/synset_words.txt')
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    get_ipython().system(u'../data/ilsvrc12/get_ilsvrc_aux.sh')
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')



def objective_L2(dst):
    dst.diff[:] = dst.data 

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

def deepdream(net, base_img, iter_n=10, octave_n=4, octave_scale=1.4, 
              end='inception_4c/output', clip=True, **step_params):
    # prepare base images for all octaves
    octaves = [preprocess(net, base_img)]
    for i in xrange(octave_n-1):
        octaves.append(nd.zoom(octaves[-1], (1, 1.0/octave_scale,1.0/octave_scale), order=1))
    
    src = net.blobs['data']
    detail = np.zeros_like(octaves[-1]) # allocate image for network-produced details
    for octave, octave_base in enumerate(octaves[::-1]):
        h, w = octave_base.shape[-2:]
        if octave > 0:
            # upscale details from the previous octave
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(detail, (1, 1.0*h/h1,1.0*w/w1), order=1)

        src.reshape(1,3,h,w) # resize the network's input image size
        src.data[0] = octave_base+detail
        for i in xrange(iter_n):
            make_step(net, end=end, clip=clip, **step_params)
            
            # visualization
            vis = deprocess(net, src.data[0])
            if not clip: # adjust image contrast if clipping is disabled
                vis = vis*(255.0/np.percentile(vis, 99.98))
            #showarray(vis)
            #print octave, i, end, vis.shape
            clear_output(wait=True)
            
        # extract details produced on the current octave
        detail = src.data[0]-octave_base
    # returning the resulting image
    return deprocess(net, src.data[0])


def do_it(num_nodes,layer):
    img_path = opj(home_path,'scratch/2015/8/19/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(1):#(num_nodes):
        mask7 = np.zeros((1,num_nodes))
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7
        net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
        net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        i_max = 100
        pb = ProgressBar(i_max)
        for i in range(i_max):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            pb.animate(i+1)
        print((model_folders[MODEL_NUM],n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

def do_it2(layer,net,iter_n):
    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,'scratch/2015/8/18/bvlc_reference_caffenet/'+layer)
    unix('mkdir -p ' + img_path)
    for n in range(layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7
        net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
        net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            pb.animate(i+1)
        print((model_folders[MODEL_NUM],n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

def do_it3(layer,net,iter_n,start=0):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,'scratch/2015/9/9/'+model_folders[MODEL_NUM]+'/'+layer.replace('/','-'))
    unix('mkdir -p ' + img_path)
    for n in range(start,layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7

        try:
            cimg = caffe.io.load_image(opj(img_path,str(n)+'.png'))
            net.blobs['data'].reshape(1,3,227,227)
            net.blobs['data'].data[...] = transformer.preprocess('data', cimg)
        except:
            net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
            net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
            net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

        pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(net,end=layer,objective=objective_kz7)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            if np.mod(i,10.0)==0:
                pb.animate(i+1)
        print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.png'),img)

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




#############################
if False:
    MODEL_NUM = 0
    net = get_net(MODEL_NUM)

    print(np.shape(net.blobs['data'].data))
    src = net.blobs['data']
    src.reshape(1,3,227,227)
    print(np.shape(net.blobs['data'].data))

    for i in range(100000):
        for l in ['prob']:
            try:
               do_it3(l,net,100,0)
            except:
                print('Exception')
    #do_it3('conv3',net,100)


if True:
    MODEL_NUM = 3
    net = get_net(MODEL_NUM)
    print(np.shape(net.blobs['data'].data))
    src = net.blobs['data']
    src.reshape(1,3,227,227)
    print(np.shape(net.blobs['data'].data))

    for l in ['fc6']:
        do_it3(l,net,2000,0)
