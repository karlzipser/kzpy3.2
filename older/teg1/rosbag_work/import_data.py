#! /usr/bin/python


#$ python kzpy3/teg1/rosbag_work/import_data.py /media/karlzipser/rosbags ~/Desktop/temp_bag; python kzpy3/teg1/rosbag_work/multi_folder_preprocess.py ~/Desktop/temp_bag/

from kzpy3.utils import *

print sys.argv[1]

print sys.argv[2]



path_to_rosbag_folders = sys.argv[1] #"/media/karlzipser/rosbags"

dest_rosbag_folders_path = sys.argv[2] #opjD('temp_rosbag_folder')
rosbag_folders = gg(opj(path_to_rosbag_folders,'*'))

for f in sorted(rosbag_folders):
	if 'lost+found' not in f:
		raw_bag_files = gg(opj(f,'*.bag'))
		print(d2s(f.split('/')[-1],len(raw_bag_files)))
		unix(d2s('scp -r',f,dest_rosbag_folders_path))

rosbag_folders = gg(opj(dest_rosbag_folders_path,'*'))
for f in sorted(rosbag_folders):
		bags = gg(opj(f,'*.bag'))
		for b in sorted(bags):
			unix(d2s('rosbag reindex',opj(f,b)))
			unix(d2s('rm',opj(f,b.replace('.bag','')+'.orig.bag')))


"""
path = '/home/karlzipser/Desktop/bair_car_rescue/data/bair_car_data'
folders =  gg(opjD('bair_car_rescue/bair_car_data/*'))

 
ctr = 0
for f in folders:
	#p = gg(path+'/'+f.split('/')[-1]+'/.preprocessed/*')
	p =  gg(opjD('bair_car_rescue/bair_car_data/'+f.split('/')[-1]+'/.preprocessed/*'))
	ctr = ctr + len(p)
	print len(p)
	print (f.split('/')[-1],len(p))
print len(folders)
print ctr
print ctr/2./60.
"""

