#! /usr/bin/python

from kzpy3.teg2.data.preprocess.preprocess_bag_data import *
from kzpy3.teg2.data.access.get_data_from_bag_files import *

bag_folders = gg(opj(sys.argv[1],'*')) #gg('/home/karlzipser/Desktop/bair_car_data/*')


for b in bag_folders[:]:
        try:
        	preprocess_bag_data(b)
        except Exception,e:
        	print e
        try:
        	save_grayscale_quarter_bagfolder(b)
        except Exception,e:
        	print e

"""
 save_grayscale_quarter_bagfolder(b)
 for n in [0,2,3]:
 	b = bag_folders[n]
 	try:
 		preprocess_bag_data(b)
 		save_grayscale_quarter_bagfolder(b)
 	except:
 		pass
"""