"""
python kzpy3/caf/kaffe/y2016/m3/kaffe3_new_start.py
"""

from kzpy3.vis import *
from kzpy3.misc.progress import *
from google.protobuf import text_format
import caffe

model_names = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet',
'finetune_BarryLyndon_8Sept2015','VGG_ILSVRC_16_layers','person_clothing_bigger_18Sept2015',
'bvlc_googlenet_person','z2_color']

for m in model_names:
    exec(d2n(m,' = ',"\'",m,"\'"))



def print_solver(solver):

    print("")
    
    for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
        print(l)

    print("")
    for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
        if 'split' not in l[0]:
            print(l)


def setup_solver(solver_file_path):
    solver = caffe.SGDSolver(solver_file_path)
    print_solver(solver)
    return solver

def get_net(model_path,net_fn,param_fn):
    model_path = opj(home_path,'caffe/models',model_folder)
    net_fn   = opj(model_path,'deploy.prototxt')
    param_fn = opj(model_path,'model.caffemodel')
    # Patching model to be able to compute gradients.
    # Note that you can also manually add "force_backward: true" line to "deploy.prototxt".
    model = caffe.io.caffe_pb2.NetParameter()
    text_format.Merge(open(net_fn).read(), model)
    model.force_backward = True
    open('tmp.prototxt', 'w').write(str(model))

    solver = setup_solver(net_fn)
    #solver = caffe.Classifier('tmp.prototxt', param_fn,
    #                       mean = np.float32([104.0, 116.0, 122.0]), # ImageNet mean, training set dependent
    #                       channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB
    print fname(model_path)
    for n in solver.net.blobs.keys():
        print (np.shape(solver.net.blobs[n].data),n)
    return solver


# a couple of utility functions for converting to and from Caffe's input image layout
def preprocess(solver, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - solver.transformer.mean['data']
def deprocess(solver, img):
    return np.dstack((img + solver.transformer.mean['data'])[::-1])



def objective_L2(dst):
    dst.diff[:] = dst.data 


def make_step(solver, step_size=0.1, end='inception_4c/output', 
              jitter=32, clip=True, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = solver.net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = solver.net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    solver.net.forward(end=end)
    objective(dst)  # specify the optimization objective
    solver.net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    g_abs_mean = np.abs(g).mean()
    if not g_abs_mean == 0:
        src.data[:] += step_size/g_abs_mean * g
    else:
        print('np.abs(g).mean() == 0')

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
    """    
    if clip:
        bias = solver.net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)    
    """



def do_it3(model_folder,dst_path,layer,solver,iter_n,start=0):

    transformer = caffe.io.Transformer({'data': solver.net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    layer_shape=list(np.shape(solver.net.blobs[layer].data));
    layer_shape[0] = 1
    layer_shape = tuple(layer_shape)
    img_path = opj(home_path,dst_path,model_folder+'/'+layer.replace('/','-'))
    unix('mkdir -p ' + img_path)
    for n in range(start,layer_shape[1]):#(num_nodes):
        mask7 = np.zeros(layer_shape)
        #n = np.random.randint(1000)
        mask7[:,n] = 1.0
        def objective_kz7(dst):
            dst.diff[:] = dst.data * mask7

        try:
            cimg = caffe.io.load_image(opj(img_path,str(n)+'.png'))
            solver.net.blobs['data'].reshape(1,3,227,227)
            solver.net.blobs['data'].data[...] = transformer.preprocess('data', cimg)
        except:
            solver.net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(solver.net.blobs['data'].data[0][1,:,:]))
            solver.net.blobs['data'].data[0][1,:,:] = 1.0*solver.net.blobs['data'].data[0][0,:,:]
            solver.net.blobs['data'].data[0][2,:,:] = 1.0*solver.net.blobs['data'].data[0][0,:,:]

        pb = ProgressBar(iter_n)
        for i in range(iter_n):
            make_step(solver,end=layer,objective=objective_kz7)
            src = solver.net.blobs['data']
            #vis = deprocess(solver, src.data[0])
            if np.mod(i,10.0)==0:
                pb.animate(i+1)
        print((model_folder,layer,n))
        vis = deprocess(solver, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        mi(img,opj(img_path,str(n)+'.png'));pause(0.01)
        #imsave(opj(img_path,str(n)+'.png'),img)



#############################
if True:
    model_folder = bvlc_googlenet_person
    model_path = opj(home_path,'caffe/models',model_folder)
    net_fn   = opj(model_path,'temp_solver.prototxt')
    param_fn = opj(model_path,'model.caffemodel')

    solver = setup_solver(net_fn)
    #solver = get_net(model_path,net_fn,param_fn)

    print(np.shape(solver.net.blobs['data'].data))
    src = solver.net.blobs['data']
    src.reshape(1,3,227,227)
    print(np.shape(solver.net.blobs['data'].data))

    for l in ['inception_3a/5x5']:#['inception_4e/output']:#['fc8']:
        do_it3(model_folder,'scratch/2017/2/9',l,solver,100,2)


