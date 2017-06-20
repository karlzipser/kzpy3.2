# These examples are from various files distributed with caffe

from kzpy3.utils import *
import caffe













def get_sessions_dic(RPi_sessions_path):
    sessions_dic,_ = dir_as_dic_and_list(RPi_sessions_path)
    for k in sessions_dic:
        print(d2s('***',k))
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
def rnd_img_name(sessions_dic):
    ses = sessions_dic.keys()
    lses = len(ses)
    k = ses[np.random.randint(lses)]
    lnm = len(sessions_dic[k]['name_list'])
    i = np.random.randint(lnm)
    f = sessions_dic[k]['name_list'][i]
    return (k,i,f)
def get_img_lst_and_target_lst(sessions_dic):
    success = False
    while success == False:
        try:
            success = True
            k,i,f = rnd_img_name(sessions_dic)
            rng = range(i,i+20)
            flst = []
            clst = []
            for j in rng:
                f = sessions_dic[k]['name_list'][j]
                c = sessions_dic[k]['name_dic'][f]['cmd']
                if c[0] < 1:
                    success = False
                    #print 'Failed!!!'
                    break
                else:
                    flst.append(f)
                    clst.append(c)
            if success:
                #print 'success'
                #for q in zip(flst,clst):
                #    print q
                img_lst = []
                for f in flst[:9]:
                    if type(sessions_dic[k]['name_dic'][f]['img']) == str:
                        img = imread(sessions_dic[k]['name_dic'][f]['img'])
                        sessions_dic[k]['name_dic'][f]['img'] = img
                    img_lst.append(sessions_dic[k]['name_dic'][f]['img'])    
        except:
            success = False
    target_lst = []
    for c in clst:
        t =  (c[3]/10.0 - 7.2) / (11.7-7.2)
        if t < 0 or t > 1:
            raise ValueError('!!!!!!!!!!!! t < 0 or t > 1')
        target_lst.append(t)
    return img_lst,target_lst

#sessions_dic = get_sessions_dic(opjh('Desktop/RPi_data'))
sessions_dic = False


"""
# making mask from jpg:
mask = imread('/Users/karlzipser/Desktop/mask.jpg')
mask = mask / 255.0
mask = 1.0 - mask
mask.max()
mask.min()
"""

mask = np.load(opjh('Desktop/mask.npy'))

mask = mask[:,:,0]











ctr = 0
last_time = time.time()



target_lst = []

class SimpleLayer4(caffe.Layer):
    def setup(self, bottom, top):
        global sessions_dic
        if not sessions_dic:
            print('Loading sessions_dic:')
            sessions_dic = get_sessions_dic(opjh('Desktop/RPi_data'))
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst
        global ctr,last_time,mask
        if np.mod(ctr,10) == 0:
            print time.time()-last_time
            last_time = time.time()
        img_lst,target_lst = get_img_lst_and_target_lst(sessions_dic)
        x1 = 0
        x2 = x1+298
        y1 = 0
        y2 = y1+224
        for i in range(9):
            top[0].data[0,i,:,:] = (img_lst[i][:,:,1]/255.0-0.5)*mask
        ctr += 1
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


#img_path = opjD('temp_data') #opjh('scratch/2015/11/RPi_images/')
img_path = opjh('scratch/2015/11/RPi_images/')

img_dic = {}
def get_img_lst_and_target_lst_real_time():
    global img_dic
    _,img_names = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
    old_img_names = img_names[:-9]
    img_names = img_names[-9:]
    img_lst = []
    for n in img_names:
        if n not in img_dic:
            img_dic[n] = imread(opj(img_path,'not_yet_viewed',n))
        img_lst.append(img_dic[n])
    #print img_names
    #print(len(img_lst))
    for n in img_dic.keys():
        if n not in img_names:
            del img_dic[n]
    #for n in old_img_names:
    #    unix(d2s('mv',opj(img_path,'not_yet_viewed',n),opj(img_path,'viewed')),False)
    target_lst = zeros(20,'float')
    return img_lst,target_lst



class SimpleLayer4_DEPLOY(caffe.Layer):
    """"""
    def setup(self, bottom, top):
        pass
    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    def forward(self, bottom, top):
        global target_lst
        global ctr,last_time,mask
        img_lst,target_lst = get_img_lst_and_target_lst_real_time()
        x1 = 0
        x2 = x1+298
        y1 = 0
        y2 = y1+224
        for i in range(9):
            top[0].data[0,i,:,:] = (img_lst[i][:,:,1]/255.0-0.5)*mask
        ctr += 1
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

