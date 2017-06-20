# These examples are from various files distributed with caffe

from kzpy3.RPi3.view_drive_data_caffe import *
import caffe
from kzpy3.utils import *

target_lst = []
M_img_lst = []
C_img_lst = []

M_ctr = 0
C_ctr = 0
last_time = time.time()


class M_SimpleLayer4(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst
        global M_img_lst
        global C_img_lst
        global M_ctr,last_time
        if np.mod(M_ctr,100) == 0:
            print time.time()-last_time
            last_time = time.time()
        M_img_lst,C_img_lst,target_lst=get_caffe_input_target(img_dic,steer_bins,all_runs_dic,CAFFE_FRAME_RANGE)
        for i in range(len(M_img_lst)): #range(9):
            top[0].data[0,i,:,:] = M_img_lst[i]
        M_ctr += 1
        assert(M_ctr == 1+C_ctr)
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

class C_SimpleLayer4(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global C_img_lst
        global C_ctr
        for i in range(len(C_img_lst)): #range(9):
            top[0].data[0,i,:,:] = C_img_lst[i]
        C_ctr += 1
        assert(M_ctr == C_ctr)
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer



class SimpleLayer5(caffe.Layer):
    """"""
    
    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        global target_lst
        for i in range(len(target_lst)):
            top[0].data[0,i] = target_lst[i]

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

