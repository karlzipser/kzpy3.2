from kzpy3.utils import *
from kzpy3.misc.progress import *

from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format
import caffe

model_folders = ['bvlc_googlenet','googlenet_places205','bvlc_reference_caffenet',
'finetune_BarryLyndon_8Sept2015','VGG_ILSVRC_16_layers','person_clothing_bigger_18Sept2015',
'bvlc_googlenet_person']

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
def backprop_diffs_to_data(model_name,layers,objective_dic,net,iter_n,img_path,opt_name=None):
    
    objectives = []
    for l in layers:
        objectives.append(objective_dic[l])

    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))
    transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
    
    unix('mkdir -p ' + img_path)

    if opt_name:
        img_path = opj(img_path,opt_name)
    else:
        img_path += '/'+'-'.join(layers).replace('/','-')# 'layer' #'/'+layer.replace('/','-')


    net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(net.blobs['data'].data[0][1,:,:]))
    net.blobs['data'].data[0][1,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]
    net.blobs['data'].data[0][2,:,:] = 1.0*net.blobs['data'].data[0][0,:,:]

    pb = ProgressBar(iter_n)
    print(d2c(model_name,' '.join(layers)))
    print(d2s('\tstart =',time.ctime()))
    save_time = time.time()
    n = 0
    for i in range(iter_n):
        for layer,objective in zip(layers,objectives):
            valid = make_step2(net,end=layer,objective=objective)
            src = net.blobs['data']
            #grayscale = src.data[0].mean(axis=0)
            #src.data[0][0,:,:] = grayscale
            #src.data[0][1,:,:] = grayscale
            #src.data[0][2,:,:] = grayscale

            src.data[0] = 200*z2o(zscore(src.data[0],2.5))-100

            if np.mod(i,10.0)==0:
                if home_path != cluster_home_path:
                    pb.animate(i+1)
            if not valid:
                print('make_step not valid.')
                break
            
            if home_path != cluster_home_path:
                if time.time()-save_time > 1:
                    vis = deprocess(net, src.data[0])
                    img = np.uint8(255*z2o(zscore(vis,2.5)))
                    imsave(opj(img_path+'.png'),img)
                    save_time = time.time()
    print(d2s('\tend =',time.ctime()))
    print((model_name,layer,n))#,labels[n]))
    vis = deprocess(net, src.data[0])
    img = np.uint8(np.clip(vis, 0, 255))
    imsave(opj(img_path+'.png'),img)
#
##########################################################



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

def print_def_code(the_layers):
    ctr = 0
    print('objective_dic = {}')
    for l in the_layers:
        print(d2n('lay',ctr,""" = '""",l,"""'"""))
        print(d2n('a',ctr,' = activations[lay',ctr,']/(10.0*activations[lay',ctr,'].max())'))
        print(d2n('def obj',ctr,'(dst):\n\tdst.diff[:] = a',ctr))
        print(d2n('objective_dic[lay',ctr,'] = obj',ctr))
        ctr += 1
#
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
    jitter=1,
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



##########################################################
#
def get_objective_dic(model_name,activations):

    if model_name == 'bvlc_googlenet_person':
        '''
        This code generated by print_def_code
        '''
        objective_dic = {}
        lay0 = 'conv1/7x7_s2'
        a0 = activations[lay0]/(10.0*activations[lay0].max())
        def obj0(dst):
            dst.diff[:] = dst.data * a0
        objective_dic[lay0] = obj0
        lay1 = 'conv2/3x3'
        a1 = activations[lay1]/(10.0*activations[lay1].max())
        def obj1(dst):
            dst.diff[:] = a1
        objective_dic[lay1] = obj1
        lay2 = 'inception_3a/1x1'
        a2 = activations[lay2]/(10.0*activations[lay2].max())
        def obj2(dst):
            dst.diff[:] = dst.data * a2#a2
        objective_dic[lay2] = obj2
        lay3 = 'inception_3a/3x3'
        a3 = activations[lay3]/(10.0*activations[lay3].max())
        def obj3(dst):
            dst.diff[:] = a3
        objective_dic[lay3] = obj3
        lay4 = 'inception_3a/5x5'
        a4 = activations[lay4]/(10.0*activations[lay4].max())
        def obj4(dst):
            dst.diff[:] = a4
        objective_dic[lay4] = obj4
        lay5 = 'inception_3a/output'
        a5 = activations[lay5]/(10.0*activations[lay5].max())
        def obj5(dst):
            dst.diff[:] = a5
        objective_dic[lay5] = obj5
        lay6 = 'inception_3b/1x1'
        a6 = activations[lay6]/(10.0*activations[lay6].max())
        def obj6(dst):
            dst.diff[:] = dst.data * a6#a6
        objective_dic[lay6] = obj6
        lay7 = 'inception_3b/3x3'
        a7 = activations[lay7]/(10.0*activations[lay7].max())
        def obj7(dst):
            dst.diff[:] = a7
        objective_dic[lay7] = obj7
        lay8 = 'inception_3b/5x5'
        a8 = activations[lay8]/(10.0*activations[lay8].max())
        def obj8(dst):
            dst.diff[:] = a8
        objective_dic[lay8] = obj8
        lay9 = 'inception_3b/output'
        a9 = activations[lay9]/(10.0*activations[lay9].max())
        def obj9(dst):
            dst.diff[:] = a9
        objective_dic[lay9] = obj9
        lay10 = 'inception_4a/1x1'
        a10 = activations[lay10]/(10.0*activations[lay10].max())
        def obj10(dst):
            dst.diff[:] = dst.data * a10#a10
        objective_dic[lay10] = obj10
        lay11 = 'inception_4a/3x3'
        a11 = activations[lay11]/(10.0*activations[lay11].max())
        def obj11(dst):
            dst.diff[:] = a11
        objective_dic[lay11] = obj11
        lay12 = 'inception_4a/5x5'
        a12 = activations[lay12]/(10.0*activations[lay12].max())
        def obj12(dst):
            dst.diff[:] = a12
        objective_dic[lay12] = obj12
        lay13 = 'inception_4a/output'
        a13 = activations[lay13]/(10.0*activations[lay13].max())
        def obj13(dst):
            dst.diff[:] = a13
        objective_dic[lay13] = obj13
        lay14 = 'inception_4b/1x1'
        a14 = activations[lay14]/(10.0*activations[lay14].max())
        def obj14(dst):
            dst.diff[:] = dst.data * a14#a14
        objective_dic[lay14] = obj14
        lay15 = 'inception_4b/3x3'
        a15 = activations[lay15]/(10.0*activations[lay15].max())
        def obj15(dst):
            dst.diff[:] = a15
        objective_dic[lay15] = obj15
        lay16 = 'inception_4b/5x5'
        a16 = activations[lay16]/(10.0*activations[lay16].max())
        def obj16(dst):
            dst.diff[:] = a16
        objective_dic[lay16] = obj16
        lay17 = 'inception_4c/1x1'
        a17 = activations[lay17]/(10.0*activations[lay17].max())
        def obj17(dst):
            dst.diff[:] = dst.data * a17#a17
        objective_dic[lay17] = obj17
        lay18 = 'inception_4c/3x3'
        a18 = activations[lay18]/(10.0*activations[lay18].max())
        def obj18(dst):
            dst.diff[:] = a18
        objective_dic[lay18] = obj18
        lay19 = 'inception_4c/5x5'
        a19 = activations[lay19]/(10.0*activations[lay19].max())
        def obj19(dst):
            dst.diff[:] = a19
        objective_dic[lay19] = obj19
        lay20 = 'inception_4c/output'
        a20 = activations[lay20]/(10.0*activations[lay20].max())
        def obj20(dst):
            dst.diff[:] = a20
        objective_dic[lay20] = obj20
        lay21 = 'inception_4d/1x1'
        a21 = activations[lay21]/(10.0*activations[lay21].max())
        def obj21(dst):
            dst.diff[:] = dst.data * a21#a21
        objective_dic[lay21] = obj21
        lay22 = 'inception_4d/3x3'
        a22 = activations[lay22]/(10.0*activations[lay22].max())
        def obj22(dst):
            dst.diff[:] = a22
        objective_dic[lay22] = obj22
        lay23 = 'inception_4d/5x5'
        a23 = activations[lay23]/(10.0*activations[lay23].max())
        def obj23(dst):
            dst.diff[:] = a23
        objective_dic[lay23] = obj23
        lay24 = 'inception_4d/output'
        a24 = activations[lay24]/(10.0*activations[lay24].max())
        def obj24(dst):
            dst.diff[:] = a24
        objective_dic[lay24] = obj24
        lay25 = 'inception_4e/1x1'
        a25 = activations[lay25]/(10.0*activations[lay25].max())
        def obj25(dst):
            dst.diff[:] = dst.data * a25#a25
        objective_dic[lay25] = obj25
        lay26 = 'inception_4e/3x3'
        a26 = activations[lay26]/(10.0*activations[lay26].max())
        def obj26(dst):
            dst.diff[:] = a26
        objective_dic[lay26] = obj26
        lay27 = 'inception_4e/5x5'
        a27 = activations[lay27]/(10.0*activations[lay27].max())
        def obj27(dst):
            dst.diff[:] = a27
        objective_dic[lay27] = obj27
        lay28 = 'inception_4e/output'
        a28 = activations[lay28]/(10.0*activations[lay28].max())
        def obj28(dst):
            dst.diff[:] = a28
        objective_dic[lay28] = obj28
        lay29 = 'inception_5a/1x1'
        a29 = activations[lay29]/(10.0*activations[lay29].max())
        def obj29(dst):
            dst.diff[:] = dst.data * a29#a29
        objective_dic[lay29] = obj29
        lay30 = 'inception_5a/3x3'
        a30 = activations[lay30]/(10.0*activations[lay30].max())
        def obj30(dst):
            dst.diff[:] = a30
        objective_dic[lay30] = obj30
        lay31 = 'inception_5a/5x5'
        a31 = activations[lay31]/(10.0*activations[lay31].max())
        def obj31(dst):
            dst.diff[:] = a31
        objective_dic[lay31] = obj31
        lay32 = 'inception_5a/output'
        a32 = activations[lay32]/(10.0*activations[lay32].max())
        def obj32(dst):
            dst.diff[:] = a32
        objective_dic[lay32] = obj32
        lay33 = 'inception_5b/1x1'
        a33 = activations[lay33]/(10.0*activations[lay33].max())
        def obj33(dst):
            dst.diff[:] = dst.data * a33#a33
        objective_dic[lay33] = obj33
        lay34 = 'inception_5b/3x3'
        a34 = activations[lay34]/(10.0*activations[lay34].max())
        def obj34(dst):
            dst.diff[:] = a34
        objective_dic[lay34] = obj34
        lay35 = 'inception_5b/5x5'
        a35 = activations[lay35]/(10.0*activations[lay35].max())
        def obj35(dst):
            dst.diff[:] = a35
        objective_dic[lay35] = obj35
        lay36 = 'inception_5b/output'
        a36 = activations[lay36]/(10.0*activations[lay36].max())
        def obj36(dst):
            dst.diff[:] = a36
        objective_dic[lay36] = obj36
        lay37 = 'prob'
        a37 = activations[lay37]/(10.0*activations[lay37].max())
        def obj37(dst):
            dst.diff[:] = a37
        objective_dic[lay37] = obj37

    if model_name == 'VGG_ILSVRC_16_layers':
        '''
        This code generated by print_def_code
        '''

        objective_dic = {}
        lay0 = 'conv1_1'
        a0 = activations[lay0]/(10.0*activations[lay0].max())
        def obj0(dst):
            dst.diff[:] = a0
        objective_dic[lay0] = obj0
        lay1 = 'conv1_2'
        a1 = activations[lay1]/(10.0*activations[lay1].max())
        def obj1(dst):
            dst.diff[:] = a1
        objective_dic[lay1] = obj1
        lay2 = 'conv2_1'
        a2 = activations[lay2]/(10.0*activations[lay2].max())
        def obj2(dst):
            dst.diff[:] = a2
        objective_dic[lay2] = obj2
        lay3 = 'conv2_2'
        a3 = activations[lay3]/(10.0*activations[lay3].max())
        def obj3(dst):
            dst.diff[:] = a3
        objective_dic[lay3] = obj3
        lay4 = 'conv3_1'
        a4 = activations[lay4]/(10.0*activations[lay4].max())
        def obj4(dst):
            dst.diff[:] = a4
        objective_dic[lay4] = obj4
        lay5 = 'conv3_2'
        a5 = activations[lay5]/(10.0*activations[lay5].max())
        def obj5(dst):
            dst.diff[:] = a5
        objective_dic[lay5] = obj5
        lay6 = 'conv3_3'
        a6 = activations[lay6]/(10.0*activations[lay6].max())
        def obj6(dst):
            dst.diff[:] = a6
        objective_dic[lay6] = obj6
        lay7 = 'conv4_1'
        a7 = activations[lay7]/(10.0*activations[lay7].max())
        def obj7(dst):
            dst.diff[:] = a7
        objective_dic[lay7] = obj7
        lay8 = 'conv4_2'
        a8 = activations[lay8]/(10.0*activations[lay8].max())
        def obj8(dst):
            dst.diff[:] = a8
        objective_dic[lay8] = obj8
        lay9 = 'conv4_3'
        a9 = activations[lay9]/(10.0*activations[lay9].max())
        def obj9(dst):
            dst.diff[:] = a9
        objective_dic[lay9] = obj9
        lay10 = 'conv5_1'
        a10 = activations[lay10]/(10.0*activations[lay10].max())
        def obj10(dst):
            dst.diff[:] = a10
        objective_dic[lay10] = obj10
        lay11 = 'conv5_2'
        a11 = activations[lay11]/(10.0*activations[lay11].max())
        def obj11(dst):
            dst.diff[:] = a11
        objective_dic[lay11] = obj11
        lay12 = 'conv5_3'
        a12 = activations[lay12]/(10.0*activations[lay12].max())
        def obj12(dst):
            dst.diff[:] = a12
        objective_dic[lay12] = obj12
        lay13 = 'fc6'
        a13 = activations[lay13]/(10.0*activations[lay13].max())
        def obj13(dst):
            dst.diff[:] = a13
        objective_dic[lay13] = obj13
        lay14 = 'fc7'
        a14 = activations[lay14]/(10.0*activations[lay14].max())
        def obj14(dst):
            dst.diff[:] = a14
        objective_dic[lay14] = obj14
        lay15 = 'fc8'
        a15 = activations[lay15]/(10.0*activations[lay15].max())
        def obj15(dst):
            dst.diff[:] = a15
        objective_dic[lay15] = obj15
        lay16 = 'prob'
        a16 = activations[lay16]/(10.0*activations[lay16].max())
        def obj16(dst):
            dst.diff[:] = a16#dst.data * a16#
        objective_dic[lay16] = obj16

    if model_name == 'bvlc_reference_caffenet':
        '''
        This code generated by print_def_code
        '''
        objective_dic = {}
        lay0 = 'conv1'
        a0 = activations[lay0]/(10.0*activations[lay0].max())
        def obj0(dst):
            dst.diff[:] = dst.data * a0#
        objective_dic[lay0] = obj0
        lay1 = 'conv2'
        a1 = activations[lay1]/(10.0*activations[lay1].max())
        def obj1(dst):
            dst.diff[:] = a1
        objective_dic[lay1] = obj1
        lay2 = 'conv3'
        a2 = activations[lay2]/(10.0*activations[lay2].max())
        def obj2(dst):
            dst.diff[:] = a2#dst.data * a2
        objective_dic[lay2] = obj2
        lay3 = 'conv4'
        a3 = activations[lay3]/(10.0*activations[lay3].max())
        def obj3(dst):
            dst.diff[:] = a3
        objective_dic[lay3] = obj3
        lay4 = 'conv5'
        a4 = activations[lay4]/(10.0*activations[lay4].max())
        def obj4(dst):
            dst.diff[:] = a4#
        objective_dic[lay4] = obj4
        lay5 = 'fc6'
        a5 = activations[lay5]/(10.0*activations[lay5].max())
        def obj5(dst):
            dst.diff[:] = a5
        objective_dic[lay5] = obj5
        lay6 = 'fc7'
        a6 = activations[lay6]/(10.0*activations[lay6].max())
        def obj6(dst):
            dst.diff[:] = a6
        objective_dic[lay6] = obj6
        lay7 = 'fc8'
        a7 = activations[lay7]/(10.0*activations[lay7].max())
        def obj7(dst):
            dst.diff[:] = a7
        objective_dic[lay7] = obj7
        lay8 = 'prob'
        a8 = activations[lay8]/(10.0*activations[lay8].max())
        def obj8(dst):
            dst.diff[:] = a8
        objective_dic[lay8] = obj8   

    return objective_dic
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


