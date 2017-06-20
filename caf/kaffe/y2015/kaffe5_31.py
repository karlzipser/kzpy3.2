from kzpy3.caf.kaffe.utils_3 import *


"""
input photo
network
layersoutput folder
randomize initial data
diff weights
act weights
jitters
initial activation source
    e.g., from input photo, or from selective mask
activation_scale_factor
"""




class NetHolder(object):
    """
    """
    def __init__(self, model_name, input_img):
        self.model_name = model_name
        self.net = get_net(self.model_name)
        s = shape(self.net.blobs['data'])
        img = imresize(input_img,(s[2],s[3],s[1]))
        self.net.blobs['data'].data[0,0,:,:] =img[:,:,2]
        self.net.blobs['data'].data[0,1,:,:] =img[:,:,1]
        self.net.blobs['data'].data[0,2,:,:] =img[:,:,0]
        self.net.forward();
        self.activations = {}
        activation_scale_factor = 0.0
        if True:
            for k in self.net.blobs.keys():
                self.activations[k] = activation_scale_factor * self.net.blobs[k].data.copy()
        if True:
            self.activations['inception_5a/1x1'][0,0,:,:]= 1.0 

    def copy_data(self,net):
        self.net.blobs['data'].data[:] = net.blobs['data'].data[:].copy()

    def randomize_input(self):
        self.net.blobs['data'].data[0][0,:,:] = 225*np.random.random(np.shape(self.net.blobs['data'].data[0][1,:,:]))
        self.net.blobs['data'].data[0][1,:,:] = 225*np.random.random(np.shape(self.net.blobs['data'].data[0][1,:,:]))
        self.net.blobs['data'].data[0][2,:,:] = 225*np.random.random(np.shape(self.net.blobs['data'].data[0][1,:,:]))

    def backprop_diffs_to_data(self,layers,jitters,dst_params,act_params,iter_n,img_path,opt_name=None):
        '''
                objective_dic = {}
                lay0 = 'conv1/7x7_s2'
                a0 = activations[lay0]/(10.0*activations[lay0].max())
                def obj0(dst):
                    dst.diff[:] = a0
                objective_dic[lay0] = obj0
        '''    
        objectives = []
        for l,d,a in zip(layers,dst_params,act_params):
            f = """
print(d2s('The layer is',l))

a_"""+l.replace('/','_')+""" = self.activations[l]
print(shape(a_"""+l.replace('/','_')+"""))
def obj_"""+l.replace('/','_')+"""(dst):
    global a_"""+l.replace('/','_')+"""
    #print('here I am!!!!!!!!!!!!')
    dst.diff[:] = """+str(d)+"""*dst.data * a_"""+l.replace('/','_')+""" + """+str(a)+"""*a_"""+l.replace('/','_')+"""
objectives.append(obj_"""+l.replace('/','_')+""")
"""
            exec(f)
            print(objectives)

        transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2,0,1))
        transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
        transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
        
        unix('mkdir -p ' + img_path)

        if opt_name:
            img_path = opj(img_path,opt_name)
        else:
            img_path += '/'+'-'.join(layers).replace('/','-')# 'layer' #'/'+layer.replace('/','-')

        pb = ProgressBar(iter_n)
        print(d2c(self.model_name,' '.join(layers)))
        print(d2s('\tstart =',time.ctime()))
        save_time = time.time()
        n = 0
        src = self.net.blobs['data']
        #src.data[0] = 200*z2o(zscore(src.data[0],2.5))-100
        #print(d2s('shape(src.data[0])=',shape(src.data[0])))
        src_means = (src.data[0][0,:,:].mean(),src.data[0][1,:,:].mean(),src.data[0][2,:,:].mean())
        src_stds = (src.data[0][0,:,:].std(),src.data[0][1,:,:].std(),src.data[0][2,:,:].std())
        print(src_means,src_stds)


        src = self.net.blobs['data']
        src.data[0][0,:,:] = zscore(src.data[0][0,:,:],2.5)
        src.data[0][1,:,:] = zscore(src.data[0][1,:,:],2.5)
        src.data[0][2,:,:] = zscore(src.data[0][2,:,:],2.5)
        src.data[0][0,:,:] *= src_stds[0]
        src.data[0][0,:,:] += src_means[0]
        src.data[0][1,:,:] *= src_stds[1]
        src.data[0][1,:,:] += src_means[1]
        src.data[0][2,:,:] *= src_stds[2]
        src.data[0][2:,:] += src_means[2]


        vis = deprocess(self.net, src.data[0])
        img = np.uint8(255*z2o(zscore(vis,2.5)))
        imsave(opj(img_path+'.png'),img)
        for i in range(iter_n):
            for layer,jitter,objective,dst_param,act_param in zip(layers,jitters,objectives,dst_params,act_params):
                #print((layer,jitter,objective))
                valid = make_step2(self.net,end=layer,objective=objective,jitter=jitter,clip=False,step_size=dst_param+act_param )
                src = self.net.blobs['data']
                #grayscale = src.data[0].mean(axis=0)
                #src.data[0][0,:,:] = grayscale
                #src.data[0][1,:,:] = grayscale
                #src.data[0][2,:,:] = grayscale

                #src.data[0] = 200*z2o(zscore(src.data[0],2.5))-100
                src.data[0][0,:,:] = zscore(src.data[0][0,:,:],2.5)
                src.data[0][1,:,:] = zscore(src.data[0][1,:,:],2.5)
                src.data[0][2,:,:] = zscore(src.data[0][2,:,:],2.5)
                src.data[0][0,:,:] *= src_stds[0]
                src.data[0][0,:,:] += src_means[0]
                src.data[0][1,:,:] *= src_stds[1]
                src.data[0][1,:,:] += src_means[1]
                src.data[0][2,:,:] *= src_stds[2]
                src.data[0][2:,:] += src_means[2]

                if np.mod(i,10.0)==0:
                    if home_path != cluster_home_path:
                        pb.animate(i+1)
                if not valid:
                    print('make_step not valid.')
                    break
                
                if home_path != cluster_home_path:
                    if time.time()-save_time > 1:
                        vis = deprocess(self.net, src.data[0])
                        img = np.uint8(255*z2o(zscore(vis,2.5)))
                        imsave(opj(img_path+'.png'),img)
                        save_time = time.time()
        print(d2s('\tend =',time.ctime()))
        print((self.model_name,layer,n))#,labels[n]))
        #vis = deprocess(net, src.data[0])
        #img = np.uint8(np.clip(vis, 0, 255))
        #imsave(opj(img_path+'.png'),img)
#
##########################################################




# - Select model
#model_name = 'VGG_ILSVRC_16_layers'
#model_name = 'bvlc_googlenet_person'
# model_name = 'bvlc_googlenet'
#model_name = 'googlenet_places205'
#model_name = 'bvlc_reference_caffenet'
#net = get_net(model_name)

# - Select input image and get it into network
img_name = 'cat.jpg'
img = imread(opjh('caffe/examples/images',img_name))#'Desktop/np.jpg')) #'Desktop/np.jpg')) #'Desktop/np.jpg')) #
img = img[:,:,:3]
'''
s = shape(net.blobs['data'])
img = imresize(img,(s[2],s[3],s[1]))
net.blobs['data'].data[0,0,:,:] =img[:,:,2]
net.blobs['data'].data[0,1,:,:] =img[:,:,1]
net.blobs['data'].data[0,2,:,:] =img[:,:,0]
net.forward();

# - Get and preprocess net activations
activations = {}
activation_scale_factor = 1.0
if True:
    for k in net.blobs.keys():
        activations[k] = activation_scale_factor * net.blobs[k].data.copy()
if False:
    activations['inception_3a/1x1'][0,15,3,3]= 1.0 
'''

if __name__ == '__main__':
    nh0 = NetHolder('bvlc_googlenet_person',img)
    nh0.randomize_input()
    #nh1 = NetHolder('googlenet_places205',img)

    for i in range(1):
        nh0.backprop_diffs_to_data(
            ['inception_5a/1x1'],#,'inception_4a/1x1','inception_4b/1x1','inception_4b/1x1','inception_4c/1x1','inception_4d/1x1','inception_4e/1x1'],#VGG_convs,#['conv3_1','conv3_2','conv4_1','conv4_2','conv5_1'],#ml,##['conv3_1'],#ml,#['conv1_1','conv1_2','conv2_1','conv2_2','conv3_1','conv3_2'],#, 'conv2/3x3'],#, 'inception_3a/1x1', 'inception_3a/3x3', 'inception_3a/5x5','inception_3a/output'],# ml,
            [5],
            [1.0],#[0.0,0.1,0.1,0.1,0.1,0.1,0.4,0.4,0.4,0.4,0.4],
            [1.0],#[0.4,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],
            5000,
            opjh('scratch/2015/10/26/temp'),#,model_name),
            'temp') #.'.join([img_name,'prob']))# 'to 10')


    '''
    for i in range(1):
        backprop_diffs_to_data(
            model_name,
            nh.activations,
            ['inception_4a/1x1'],#,'inception_4a/1x1','inception_4b/1x1','inception_4b/1x1','inception_4c/1x1','inception_4d/1x1','inception_4e/1x1'],#VGG_convs,#['conv3_1','conv3_2','conv4_1','conv4_2','conv5_1'],#ml,##['conv3_1'],#ml,#['conv1_1','conv1_2','conv2_1','conv2_2','conv3_1','conv3_2'],#, 'conv2/3x3'],#, 'inception_3a/1x1', 'inception_3a/3x3', 'inception_3a/5x5','inception_3a/output'],# ml,
            [1,6,10,15,20,25,25,25,25,25,25,25,25,25,25],
            [0.0,0.0,0.0,0.4,0.5,0.6,0.7,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],#[0.0,0.1,0.1,0.1,0.1,0.1,0.4,0.4,0.4,0.4,0.4],
            [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],#[0.4,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],
            nh.net,1000,
            opjh('scratch/2015/10/20',model_name),
            'temp') #.'.join([img_name,'prob']))# 'to 10')
    '''
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