# These examples are from various files distributed with caffe

from kzpy3.utils import *
import caffe




def get_sessions_dic(RPi_sessions_path):
    sessions_dic,_ = dir_as_dic_and_list(RPi_sessions_path)
    for k in sessions_dic:
        sessions_dic[k] = {}
        _,jpg_lst = dir_as_dic_and_list(opj(RPi_sessions_path,k,'jpg'))
        sessions_dic[k]['name_list'] = jpg_lst
        sessions_dic[k]['name_dic'] = {}
        for f in sessions_dic[k]['name_list']:
            sessions_dic[k]['name_dic'][f] = {}
        for d in reversed(
            txt_file_to_list_of_strings(opj(RPi_sessions_path,k,'session_list-'+k+'.txt'))):
            f = d.split(' ')[0]
            c = d.split(' ')[-4:]
            if f in sessions_dic[k]['name_dic']:
                for i in range(len(c)):
                    c[i] = int(c[i])
                sessions_dic[k]['name_dic'][f]['cmd'] = c
                sessions_dic[k]['name_dic'][f]['img'] = opj(RPi_sessions_path,k,'jpg',f)
    return sessions_dic

sessions_dic = get_sessions_dic(opjh('Desktop/RPi_data'))


def rnd_img_name(sessions_dic):
    ses = sessions_dic.keys()
    lses = len(ses)
    k = ses[np.random.randint(lses)]
    lnm = len(sessions_dic[k]['name_list'])
    i = np.random.randint(lnm)
    f = sessions_dic[k]['name_list'][i]
    return (k,i,f)















target = 0

class SimpleLayer4(caffe.Layer):
    """"""
    
    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        global target
        #xy_offset[0] = np.random.randint(3)
        #xy_offset[1] = np.random.randint(3)
#        img = imread(opjD('img.jpg'))

        k,i,f=rnd_img_name(sessions_dic)
        print sessions_dic[k]['name_dic'][f]['cmd']
        print sessions_dic[k]['name_dic'][f]['img']
        img = imread(sessions_dic[k]['name_dic'][f]['img'])
        target = (sessions_dic[k]['name_dic'][f]['cmd'][3]/10.0 - 7.2) / (11.7-7.2)
        if target < 0:
            target = 0.5
        print(d2s('target =',target))
        x1 = 0
        x2 = x1+298
        y1 = 0
        y2 = y1+224
        #print(shape(top[0].data))
        #print(shape(img))
        top[0].data[0,0,:,:] = img[:,:,2]/255.0-0.5
        top[0].data[0,1,:,:] = img[:,:,1]/255.0-0.5
        top[0].data[0,2,:,:] = img[:,:,0]/255.0-0.5
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer5(caffe.Layer):
    """"""
    
    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        global target
        print(d2s('****************** target =',target))
        top[0].data[0,0] = target


            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer

