from kzpy3.utils import *
import imghdr
import hashlib
from PIL import Image

img_dic = {}

'''
things_to_ignore_in_root = ['/.','/Library/','Applications',
                            'nltk','bptt','Music','Movies','kzpy3','p_images',
                            'caffenet-yos','caffe','scratch','1March2014 RF paper','analysis.matlab3',
                            '21Jan2015 VS298 seminar','SUBMITTED NSF GRANT','rtfd',
                           'deep-visualization-toolbox-master','neural-networks-and-deep-learning',
                            'rethinking mid-level vision','26June2015_data_processing',
                            'analysis.matlab4','deepnet_data','17June2015 surface ideas',
                            'MODVIS_talk','VSS fMRI talk','Theano_DeepLearningTutorials',
                            '3March 2015 MODVIS material PAGES.pages','21Jan2015 LITERATURE reorganized',
                            '12July2015 S7_2015 mapping initial report',
                            'deepdream-master','analysis.python','python-cogstats-master','py/2015/','19July2015 p-imaging results',
                            'SFO to Seattle','9Jan2015 fixation vs brain activity','/py/','15June2015 attend surface analysis images','13April2015 Google Faculty Award preparation folder','13March2015 VS298 visual stability presentation.key',
                           'deep-visualization-toolbox','py-2015-8 bkp',
                           '18June2015 images for scanning',
                           '24Mar2015 Eyelink workshop and other notes_files',
                           'documents-export-2015-07-21'
                           ]
'''
things_to_ignore_in_root = ['/.']
def get_img_hash_dict(

	path_to_walk = home_path,
	img_dic={},
	quiet = True,
	collect_images = False,
	img_dirs = {},
	things_to_ignore_in_root=things_to_ignore_in_root,
	min_width = 1000,
	min_height = 1000
	): # first there is the process of looking at the directories with at least one image.

	duplicates = []
	exceptions = []
	

	print_time = time.time()
	for root, dirs, files in os.walk(path_to_walk):
	    if time.time()-print_time > 5:
	        print_time = time.time()
	        print(d2s(time.ctime(),'Found',len(img_dic),'image files.'))
	    ignore = False
	    for t in things_to_ignore_in_root:
	        if t in root:
	            ignore = True
	            #print(d2s('ignoring',root))
	            break
	    if not ignore:
	        path = root.split('/')
	        for file in files:
	            try:
	                if file[0] != '.':
	                    img_type = imghdr.what(opj(root,file))
	                    if img_type:
	                        img_dirs[root] = True
	                        if collect_images:
	                            checksum = hashlib.md5(open(opj(root,file), 'rb').read()).digest()
	                            if quiet == False:
	                                print(d2s(opj(root,file),':',checksum))
	                            
	                            else:
	                                if quiet == False:
	                                    print((d2s('Duplicate found: ',opj(root,file))))
	                                duplicates.append(checksum)
	                            dic = {}
	                            dic['file'] = opj(root,file)
	                            dic['type'] = img_type
	                            im = Image.open(dic['file'])
	                            width,height = im.size
	                            if width >= min_width:
	                            	if height >= min_height:
	                            		if not img_dic.has_key(checksum):
	                                		img_dic[checksum] = []
		                            	dic['dim'] = im.size
		                            	img_dic[checksum].append(dic)
	                        else:
	                            break
	                        
	            except:
	                exceptions.append(opj(root,file))
	if collect_images:
		print(d2s(time.ctime(),'Found',len(img_dic),'image files.',len(duplicates),'duplicates.'))
	print(d2s('Found',len(img_dirs),'image directories.'))

	return img_dic,img_dirs



