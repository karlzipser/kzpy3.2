from kzpy3.utils import *
from kzpy3.misc.progress import *
#plt.ion()

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

GPU_FLAG = False

cluster_home_path = '/global/home/users/karlz'
if home_path == cluster_home_path:
    GPU_FLAG = True
    caffe.set_mode_gpu()
    caffe.set_device(0) # select GPU device if multiple devices exist

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet',
'finetune_BarryLyndon_8Sept2015','VGG_ILSVRC_16_layers','person_clothing_bigger_18Sept2015',
'bvlc_googlenet_person','nin_imagenet_conv_sandbox']

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
              jitter=32, clip=True, objective=objective_L2,z2o_g_abs_sum=1.0):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    gabs = np.abs(g)
    if gabs.sum() == 0:
        print('gabs.sum() == 0')
    
    # apply normalized ascent step to the input image
    #src.data[:] += step_size/np.abs(g).mean() * g
    src.data[:] += step_size/gabs[gabs>0].mean() * g
    
    src.data[:] *= 0.995
    #print(shape(src.data[:]))
    gray = src.data.mean(axis=1)

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
    a=0.3
    src.data[:,0,:,:] = (1.0-a) * src.data[:,0,:,:] + a * mona[:,:,0] *z2o_g_abs_sum#gray
    src.data[:,1,:,:] = (1.0-a) * src.data[:,1,:,:] + a * mona[:,:,0] *z2o_g_abs_sum#gray
    src.data[:,2:,:] = (1.0-a) * src.data[:,2,:,:] + a * mona[:,:,0] *z2o_g_abs_sum#gray
    """
    src.data[:,0,:,:] = 0.90 * src.data[:,0,:,:] + 0.1 * mona[:,:,0]* (1-mask)*z2o_g_abs_sum#gray# * (1-mask)#gray
    src.data[:,1,:,:] = 0.90 * src.data[:,1,:,:] + 0.1 * mona[:,:,0]* (1-mask)*z2o_g_abs_sum#gray# * (1-mask)#gray
    src.data[:,2:,:] = 0.90 * src.data[:,2,:,:] + 0.1 * mona[:,:,0]* (1-mask)*z2o_g_abs_sum#gray# * (1-mask)#gray
    
    src.data[:,0,:,:] = 0.99 * src.data[:,0,:,:] + 0.01 * gray
    src.data[:,1,:,:] = 0.99 * src.data[:,1,:,:] + 0.01 * gray
    src.data[:,2:,:] = 0.99 * src.data[:,2,:,:] + 0.01 * gray
    """
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)

    return g



def make_step2(net, step_size=1.5, end='inception_4c/output', 
              jitter=32, clip=True, objective=objective_L2,mask=False):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    objective(dst)  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    g = g * mask
    gabs = np.abs(g)
    if gabs.sum() == 0:
        print('gabs.sum() == 0')
    
    # apply normalized ascent step to the input image
    #src.data[:] += step_size/np.abs(g).mean() * g
    src.data[:] += step_size/gabs[gabs>0].mean() * g
    
    #src.data[:] *= 0.995
    #print(shape(src.data[:]))
    gray = src.data.mean(axis=1)

    #src.data[:,0,:,:] = 0.99 * src.data[:,0,:,:] + 0.01 * gray
    #src.data[:,1,:,:] = 0.99 * src.data[:,1,:,:] + 0.01 * gray
    #src.data[:,2:,:] = 0.99 * src.data[:,2,:,:] + 0.01 * gray

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)    

print('Reading mona .png')
mona = imread(opjD('mona_224.png'))
mona = mona[:,:,:3]
mask = 0*mona[:,:,0]
mask[50:100,50:100] = 1.0
imsave(opjD('mona_244_occluded.png'),mona[:,:,0]*(1-mask))

image_path_folders_opened = {}

def do_it3(layer,net,iter_n,start=0,end=-1,single_RF=False,multi_RF=False,x_center=-1,y_center=-1,scratch_path='scratch/2015/10/28/',img_dic={},use_mona=False):

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)

    img_path = opj(home_path,scratch_path,model_folders[MODEL_NUM]+'/'+layer.replace('/','-'))
    if img_path not in image_path_folders_opened:
        unix('mkdir -p ' + img_path)
        image_path_folders_opened[img_path] = True
        unix('open ' + img_path)
    if end == -1:
        end = layer_shape[1]
    for n in range(start,end):#[start]:#
        mask7 = np.zeros(layer_shape)
        print((model_folders[MODEL_NUM],layer,n))#,labels[n]))
        print(layer_shape)
        #n = np.random.randint(1000)
        
        if x_center < 0:
            x_center = layer_shape[2]/2
        if y_center < 0:
            y_center = layer_shape[3]/2
        print(d2s(('x_center','y_center'),(x,y)))
        if single_RF:
            mask7[:,n,x_center,y_center] = 1.0
        else:
            mask7[:,n] = 1.0

        #elif multi_RF:
        #    mask7[:,30,layer_shape[2]/2,layer_shape[3]/2] = 0.0/1.0
        #    mask7[:,30,layer_shape[2]/2,4+layer_shape[3]/2] = 1.0/1.0
        #    mask7[:,30,layer_shape[2]/2,-4+layer_shape[3]/2] = 0.0/1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7 * dst.data[:]

        #try: # Try to load existing image, otherwise make random dot pattern.
        #    cimg = caffe.io.load_image(opj(img_path,str(n)+'.png'))
        #    net.blobs['data'].reshape(1,3,224,224)
        #    net.blobs['data'].data[...] = transformer.preprocess('data', cimg)
        #except:

        if (x_center,y_center) in img_dic:
            net.blobs['data'].data[0] = img_dic[(x_center,y_center)].copy()    
        elif use_mona == False:
            net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
            net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
            net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        else:
            net.blobs['data'].data[0][0,:,:] = mona[:,:,0]
            net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
            net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
        

        pb = ProgressBar(iter_n)
        tm = str(np.int(time.time()))
        print(time_str())

        src = net.blobs['data']
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.'+str((x_center,y_center))+'.png'),img)
        g_abs_sum = 0.0*img[:,:,0]
        for i in range(iter_n):
            if i > 1:
                g = make_step(net,jitter=1,end=layer,objective=objective_kz7,clip=True,z2o_g_abs_sum=z2o(g_abs_sum))
            else:
                g = make_step(net,jitter=1,end=layer,objective=objective_kz7,clip=True)
            g_abs_sum += np.abs(g).mean(axis=0)
            #make_step2(net,jitter=1,end=layer,objective=objective_kz7,clip=True,mask=mask)
            src = net.blobs['data']
            #vis = deprocess(net, src.data[0])
            if np.mod(i,10.0)==0:
                pb.animate(i+1)
            if i < 500:
                f = 100
            elif i < 2000:
                f = 500
            else:
                f = 1000
            if True:
                if np.mod(i,20)==0:
                    vis = deprocess(net, src.data[0])
                    img = np.uint8(np.clip(vis, 0, 255))
                    #mi(img,opj(img_path,str(n)+'.png'))
                    imsave(opj(img_path,str(n)+'.'+str((x_center,y_center))+'.png'),img)
                    imsave(opj(img_path,str(n)+'.g_abs_sum.'+str((x_center,y_center))+'.png'),z2o(g_abs_sum))
                    imsave(opj(img_path,str(n)+'.mod.'+str((x_center,y_center))+'.png'),(mona[:,:,0]-mona[:,:,0].mean())*z2o(g_abs_sum)+mona[:,:,0].mean())
        img_dic[(x_center,y_center)] = net.blobs['data'].data[0].copy()
        
        vis = deprocess(net, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        #mi(img,opj(img_path,str(n)+'.png'))
        imsave(opj(img_path,str(n)+'.'+str((x_center,y_center))+'.png'),img)
        



inception_layers = [
        #'conv1/7x7_s2',
        'conv2/3x3',
        'inception_3a/1x1',
        'inception_3a/3x3',
        'inception_3a/5x5',
        'inception_3b/1x1',
        'inception_3b/3x3',
        'inception_3b/5x5',
        'inception_4a/1x1',
        'inception_4a/3x3',
        'inception_4a/5x5',
        'inception_4b/1x1',
        'inception_4b/3x3',
        'inception_4b/5x5',
        'inception_4c/1x1',
        'inception_4c/3x3',
        'inception_4c/5x5',
        'inception_4d/1x1',
        'inception_4d/3x3',
        'inception_4d/5x5',
        'inception_4e/1x1',
        'inception_4e/3x3',
        'inception_4e/5x5'
        ]
"""        ,
        'inception_5a/1x1',
        'inception_5a/3x3',
        'inception_5a/5x5',
        'inception_5b/1x1',
        'inception_5b/3x3',
        'inception_5b/5x5',
        'loss3/classifier']
"""



#############################
if True:
    MODEL_NUM = 6
    net = get_net(MODEL_NUM)

    print(np.shape(net.blobs['data'].data))
    src = net.blobs['data']
    src.reshape(1,3,224,224)
    print(np.shape(net.blobs['data'].data))

    #inception_layers.reverse()
    if GPU_FLAG:
        print("*********** Using GPU ***********")
    else:
        print("*********** Using CPU ***********")
    
    start_node = 528#423#41#267#55#55#
    for n in range(start_node,start_node+1):
        img_dic = {}
        for r in range(100):
            for x in [1]:
                for y in [1]:
                    for l in ['loss3/classifier']:#['inception_4c/5x5']:#['inception_4b/5x5']:#inception_layers:#['conv1/7x7_s2']:#['inception_5b/5x5']:#['inception_4b/5x5']:# 'inception_4b/5x5']:# 'inception_4d/5x5']:#['inception_4e/output']:#['fc8']:
                        #if l == 'loss3/classifier':
                        #    single_rf = False
                        #else:
                        #    single_rf = True
                        single_rf = False
                        
                        do_it3(l,net,2000,n,n+1,single_rf,True,x,y,'scratch/2015/11/15',img_dic,use_mona=True)

