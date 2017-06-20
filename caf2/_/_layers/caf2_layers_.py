# These examples are from various files distributed with caffe

from kzpy3.caf2.MODE import *
import caffe

target_lst_train = []
img_lst_train = []
target_lst_test = []
img_lst_test = []
ctr = 0
last_time = time.time()

N = 1000

class SimpleLayer4_train(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst_train
        global ctr,last_time
        if np.mod(ctr,N) == 0:
            print(d2s(dp(N/(time.time()-last_time),1), 'iterations per second.'))
            last_time = time.time()
        img_lst_train,target_lst_train = get_caffe_input_target(steer_bins_train,all_runs_dic_train,CAFFE_FRAME_RANGE)
        for i in range(len(img_lst)):
            top[0].data[0,i,:,:] = img_lst[i]
        ctr += 1
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff
class SimpleLayer4_test(caffe.Layer):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst_test
        global ctr,last_time
        if np.mod(ctr,N) == 0:
            print(d2s(dp(N/(time.time()-last_time),1), 'iterations per second.'))
            last_time = time.time()
        img_lst_test,target_lst_test = get_caffe_input_target(steer_bins_test,all_runs_dic_test,CAFFE_FRAME_RANGE)
        for i in range(len(img_lst)):
            top[0].data[0,i,:,:] = img_lst_test[i]
        ctr += 1
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff



class SimpleLayer5_train(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        for i in range(len(target_lst_train)):
            top[0].data[0,i] = target_lst[i]_train
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff
class SimpleLayer5_test(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        for i in range(len(target_lst_test)):
            top[0].data[0,i] = target_lst[i]_test
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff

