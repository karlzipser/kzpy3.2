#! //anaconda/bin/python

from kzpy.startup import *


# In[2]:

import numpy as np
import matplotlib.pyplot as plt

import os
# Make sure that caffe is on the python path:
caffe_root = os.path.expanduser("~")+'/caffe/'  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

import os
if not os.path.isfile(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
    print("Downloading pre-trained CaffeNet model...")
    get_ipython().system(u'../scripts/download_model_binary.py ../models/bvlc_reference_caffenet')


# In[3]:

# load labels
imagenet_labels_filename = caffe_root + 'data/ilsvrc12/synset_words.txt'
try:
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')
except:
    get_ipython().system(u'../data/ilsvrc12/get_ilsvrc_aux.sh')
    labels = np.loadtxt(imagenet_labels_filename, str, delimiter='\t')


# In[4]:

caffe.set_mode_cpu()
net = caffe.Net(caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt',
                caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel',
                caffe.TEST)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB


# In[6]:

mat = scipy.io.loadmat(home_path+'/kzpy/scripts/2Jan2014_first_run.736192.3625.vox_xys.mat')
vox_xys = mat['vox_xys']
vxys = vox_xys.copy()
vxys[:,0] -= vxys[:,0].min()
vxys[:,1] -= vxys[:,1].min()
(vxys[:,0].max(),vxys[:,0].max())
vimg = np.zeros((vxys.max()+1,vxys.max()+1))


# In[7]:

import cv2

cap = cv2.VideoCapture(0)

start_time = time.time()

while(True):
    try:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = frame[:,280:-280]

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #net.blobs['data'].reshape(1,3,227,227)
        net.blobs['data'].data[...] = transformer.preprocess('data', frame)
        out = net.forward()
        #print("Predicted class is #{}.".format(out['prob'].argmax()))    
        top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-2:-1]
        #print labels[top_k]    


        vdata_a = net.blobs['fc7'].data[0].copy()
        vdata_a = vdata_a-vdata_a.mean()
        vdata_a = vdata_a/vdata_a.std()
        vdata_a[vdata_a>3.0] = 3.0
        vdata_a[vdata_a<-3.0] = -3.0

        for i in range(np.shape(vxys)[0]):
            vimg[vxys[i,1],vxys[i,0]] = vdata_a[i]

        #feat = net.blobs['conv5'].data[0]
        #vimg = vis_square2(feat, padval=0.5)   

        #if time.time() - start_time > 60:
        #    break

        # Display the resulting frame
        cv2.imshow('frame',np.fliplr(scipy.misc.imresize(frame,25)))
        cv2.imshow('frame2',scipy.misc.imresize(vimg,300,'nearest'))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break
    except:
        print("Exception")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print("Done.")


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



