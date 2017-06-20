import caffe

#caffe.set_device(0)
caffe.set_mode_cpu()

from kzpy3.vis import *

os.chdir(home_path) # this is for the sake of the train_val.prototxt
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_no_py_layers.prototxt"))
solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_iter_11100000.caffemodel'))

for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
    print(l)
for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
    print(l)

img_top_folder = opjh('Desktop/RPi_data')
_,img_dirs = dir_as_dic_and_list(img_top_folder)
ctimes = []
for d in img_dirs:
    ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
most_recent_img_dir = img_dirs[sort_indicies[-1]]
print most_recent_img_dir
unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)

img_dic = {}

def get_caffe_input_target():
    img_lst = []
    _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
    print d2s(len(img_files),'image files')
    if len(img_files) > 9:
        img_lst = []
        for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
            # we avoid loading the most recent image to avoid 'race' conditions.
            f = img_files[i]
            if f not in img_dic:
                img_dic[f] = imread(opj(img_top_folder,most_recent_img_dir,f))
            img = img_dic[f]
            img = img.mean(axis=2)
            img = imresize(img,(56,75))/255.0-0.5
            img_lst.append(img)
        if len(img_files) > 10:
            for f in img_files[:-10]:
                os.rename(opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe',f))
                #unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    else:
        dummy = np.random.random((56,75))
        for i in range(9):
            img_lst.append(dummy)
    return img_lst


while True:
    try:
        img_lst = get_caffe_input_target()
        for i in range(len(img_lst)):
            solver.net.blobs['py_image_data'].data[0,i,:,:] = img_lst[i]
        solver.net.forward();
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    try:
        steer = solver.net.blobs['ip2'].data[0][0]
        steer -= 0.5
        steer *= 100
        steer = int(steer)
        np.save(opjh('Desktop/caffe_command.npy'),steer)
        print (steer,int(100*(solver.net.blobs['ip2'].data[0][1])),int(100*(solver.net.blobs['ip2'].data[0][2])))
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
    if len(img_dic) > 100:
        del img_dic
        img_dic = {}



