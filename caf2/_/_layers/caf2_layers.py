from kzpy3.utils import *
info_file = 'kzpy3/caf2/tmp/__info__.py'
c = txt_file_to_list_of_strings(opjh(info_file))
for e in c: exec(e)

import_str = "from kzpy3.caf2.modes.CAFFE_MODE import *"
exec(import_str.replace('CAFFE_MODE',CAFFE_MODE))

import caffe

ctr = 0
last_time = time.time()

N = 1000

layers_str = """
target_lst_PHASE = []
img_lst_PHASE = []

class SimpleLayer4_PHASE(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst_PHASE
        global ctr,last_time
        if np.mod(ctr,N) == 0:
            print(d2s(dp(N/(time.time()-last_time),1), 'iterations per second.'))
            last_time = time.time()
        img_lst_PHASE,target_lst_PHASE = get_caffe_input_target(steer_bins_PHASE,all_runs_dic_PHASE,CAFFE_FRAME_RANGE)
        for i in range(len(img_lst_PHASE)):
            top[0].data[0,i,:,:] = img_lst_PHASE[i]
        ctr += 1
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff

class SimpleLayer5_PHASE(caffe.Layer):
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        for i in range(len(target_lst_PHASE)):
            top[0].data[0,i] = target_lst_PHASE[i]
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff
"""

for phase in ['TRAIN','TEST']:
    lsr = layers_str.replace('PHASE',phase)
    exec(lsr)

