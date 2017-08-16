"""
python kzpy3/caf/kaffe/y2016/m3/kaffe3_new_start.py
"""

from kzpy3.vis import *
from kzpy3.misc.progress import *
from google.protobuf import text_format
import caffe



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
    return np.float32(np.rollaxis(img, 2)[::-1]) - solver.transformer.mean['ZED_data_pool2']
def deprocess(solver, img):
    return np.dstack((img + solver.transformer.mean['ZED_data_pool2'])[::-1])



def objective_L2(dst):
    dst.diff[:] = dst.data 


def make_step(solver, step_size=0.1, end='inception_4c/output', 
              jitter=32, clip=True, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = solver.net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = solver.net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
    print('A0');mi(src.data[0,0,:,:]);pause(0.5)       
    solver.net.forward(start='conv1',end=end)
    print('A1');mi(src.data[0,0,:,:]);pause(0.5)
    objective(dst)  # specify the optimization objective
    
    solver.net.backward(start=end,end='data')
    g = src.diff[0]
    print shape(g)
    print((g.max(),g.min()))
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



def do_it4(model_folder,dst_path,layer,solver,iter_n,start=0):

    #transformer = caffe.io.Transformer({'data': solver.net.blobs['data'].data.shape})
    #transformer.set_transpose('data', (2,0,1))
    #transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    #transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    #transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

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
            dst.diff[:] = mask7#dst.data * mask7

        for i in range(0,12):
            solver.net.blobs['data'].data[0,i,:,:] = np.random.random(np.shape(solver.net.blobs['data'].data[0,1,:,:]))-0.5

        #mi(solver.net.blobs['ZED_data_pool2'].data[0,0,:,:]);pause(0.01)
        pb = ProgressBar(iter_n)
        #print((solver.net.blobs['data'].data[0,0,:,:].min(),solver.net.blobs['data'].data[0,0,:,:].max()))
        for i in range(iter_n):
            make_step(solver,end=layer,objective=objective_kz7,jitter=1)
            src = solver.net.blobs['data']
            #vis = deprocess(solver, src.data[0])
            if np.mod(i,50.0)==0:
                pb.animate(i+1)
                #print((solver.net.blobs['data'].data[0,0,:,:].min(),solver.net.blobs['data'].data[0,0,:,:].max()))
                mi(z2o(solver.net.blobs['data'].data[0,0,:,:]));pause(0.01)
            pb.animate(i+1)
        print((model_folder,layer,n))
        vis = src.data[0]#deprocess(solver, src.data[0])
        img = np.uint8(np.clip(vis, 0, 255))
        print shape(vis)
        mi(solver.net.blobs['data'].data[0,0,:,:]);pause(0.01)#,opj(img_path,str(n)+'.png'));pause(0.01)
        #imsave(opj(img_path,str(n)+'.png'),img)



#############################
if True:
    solver_name = opjh('kzpy3/caf7/z2_color/solver_temp.prototxt')
    solver = setup_solver(solver_name)
    weights_file_path = 'kzpy3/caf5/z2_color/z2_color.caffemodel'
    solver.net.copy_from(weights_file_path)
    solver.net.params['data'][0].data[:] = 1
    solver.net.params['data'][1].data[:] = 0
    model_folder = solver_name.split('/')[-2]

    print(np.shape(solver.net.blobs['data'].data))
    src = solver.net.blobs['data']

    print(np.shape(solver.net.blobs['data'].data))

    for l in ['conv2']:
        do_it4(model_folder,'scratch/'+time_str(),l,solver,30,0)


