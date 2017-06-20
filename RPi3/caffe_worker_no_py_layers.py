import caffe
from kzpy3.vis import *

# rsync -avz ~/Desktop/RPi3_data/runs_scale_50_BW/ kzipser@redwood2.dyn.berkeley.edu:'~/Desktop/runs_scale_50_BW'

os.chdir(home_path) # this is for the sake of the train_val.prototxt
solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m2/from_mnist/original_with_accuracy/solver_11px_no_py_layers.prototxt"))
#solver = caffe.SGDSolver(opjh("kzpy3/caf/training/y2016/m3/RPi3/solver_11px_MC.prototxt"))

#solver.net.copy_from(opjh('scratch/2016/2/16/caffe/models/from_mnist/original_with_accuracy_11px_scl50_steer_only/original_with_accuracy_11px_scl50_iter_1200000.caffemodel'))
#solver.net.copy_from(opjh('scratch/2016/3/RPi3/11px_MC_rw2/11px_MC_iter_6800000.caffemodel'))
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

def get_caffe_input_target():
    img_lst = []
    _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
    if len(img_files) > 9:
        img_lst = []
        for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
            # we avoid loading the most recent image to avoid 'race' conditions.
            f = img_files[i]
            #print f
            img = imread(opj(img_top_folder,most_recent_img_dir,f))
            img = img.mean(axis=2)
            img = imresize(img,25)/255.0-0.5
            img_lst.append(img)
        if len(img_files) > 10:
            for f in img_files[:-10]:
                unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    else:
        dummy = np.random.random((56,75))
        for i in range(9):
            img_lst.append(dummy)
    for img in img_lst:
        mi(img);
        plt.pause(0.1)
    return img_lst

while True:
    try:
        img_lst = get_caffe_input_target()
        print len(img_lst)
        #print shape(solver.net.blobs['py_image_data'].data[0,i,:,:])
        #print shape(img_lst[0])
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



