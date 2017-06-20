from kzpy3.utils import *

"""
from kzpy3.teg1.rosbag_work.preprocess_bag_data import *
bag_folders = gg('/media/karlzipser/bair_car_data_4/bair_car_data/*')
for b in bag_folders[:]:
	try:
		preprocess_bag_data(b)
		save_grayscale_quarter_bagfolder(b)
	except:
		print b + ' failed.'
"""
print sys.argv[1]
bair_car_data_path = sys.argv[1]#'/media/karlzipser/rosbags/'

bair_car_data_folders = gg(opj(bair_car_data_path,'*'))

for bf in bair_car_data_folders:
	bags = gg(opj(bair_car_data_path,bf,'*.bag'))
	pklbags = gg(opj(bair_car_data_path,bf,'.preprocessed','*.bag.pkl'))
	leftpkl = gg(opj(bair_car_data_path,bf,'.preprocessed','left_image_*'))
	print (bf.split('/')[-1],len(bags),len(pklbags),len(leftpkl))