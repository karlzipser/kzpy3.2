from kzpy3.utils import *

to_do_str = """
all_runs_dic_PHASE = []
steer_bins_PHASE = []
"""
for phase in ['TRAIN','TEST']:
    lsr = to_do_str.replace('PHASE',phase)
    exec(lsr)

img_top_folder = opjh('Desktop/RPi_data')

_,img_dirs = dir_as_dic_and_list(img_top_folder)
ctimes = []
for d in img_dirs:
    ctimes.append(os.path.getmtime(opj(img_top_folder,d)))
sort_indicies = [i[0] for i in sorted(enumerate(ctimes), key=lambda x:x[1])]
most_recent_img_dir = img_dirs[sort_indicies[-1]]
print most_recent_img_dir
unix(d2s('mkdir -p',opj(img_top_folder,most_recent_img_dir+'_caffe')),False)

def get_caffe_input_target(_ignore1_,_ignore2_,_ignore3_):
    img_lst = []
    _,img_files = dir_as_dic_and_list(opj(img_top_folder,most_recent_img_dir))
    if len(img_files) > 9:
        img_lst = []
        for i in range(-10,-1): # = [-10, -9, -8, -7, -6, -5, -4, -3, -2]
            # we avoid loading the most recent image to avoid 'race' conditions.
            f = img_files[i]
            #print f
            img = imread_from_img_dic(img_dic,opj(img_top_folder,most_recent_img_dir),f)
            img = img.mean(axis=2)
            img = imresize(img,25)/255.0-0.5
            img_lst.append(img)
        if len(img_files) > 10:
            for f in img_files[:-10]:
                unix(d2s('mv',opj(img_top_folder,most_recent_img_dir,f),opj(img_top_folder,most_recent_img_dir+'_caffe')),False)
    else:
        dummy = np.random.random((112,150)) # This will not always be the right shape.
        for i in range(9):
            img_lst.append(dummy)
    return img_lst,[0,0,0]


