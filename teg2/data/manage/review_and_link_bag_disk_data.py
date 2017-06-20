from kzpy3.utils import *

"""
from kzpy3.teg1.rosbag_work.preprocess_bag_data import *
bag_folders = gg('/media/karlzipser/bair_car_data_6/bair_car_data/*')
for b in bag_folders[:]:
	try:
		preprocess_bag_data(b)
		save_grayscale_quarter_bagfolder(b)
	except:
		print b + ' failed.'
"""

bair_car_min_data_path = sys.argv[1] #'/media/karlzipser/bair_car_data_min/bair_car_data_6_min'
bair_car_data_min_links_path = sys.argv[2]

unix('mkdir -p '+bair_car_data_min_links_path)

bair_car_min_disks = gg(opj(bair_car_min_data_path,'*'))

for bcm_disks in bair_car_min_disks:
	print bcm_disks
	
	bair_car_data_folders = gg(opj(bcm_disks,'*'))

	total_pklbags = 0

	for bf in bair_car_data_folders:
		bags = gg(opj(bf,'*.bag'))
		pklbags = gg(opj(bf,'.preprocessed','*.bag.pkl'))

		pklbags_sizes = []
		for p in pklbags:
			sz = os.path.getsize(p)
			if sz > 20000000:
				total_pklbags += 1
			pklbags_sizes.append(sz)
		pklbags_sizes = np.array(pklbags_sizes)

		leftpkl = gg(opj(bf,'.preprocessed','left_image_*'))
		
		if len(pklbags_sizes) > 0:
			stats = (pklbags_sizes.min(),np.int(pklbags_sizes.mean()),pklbags_sizes.max())
			unix( d2s("ln -s",bf,opj(bair_car_data_min_links_path,bf.split('/')[-1])), False )
		else:
			stats = ('nothing')
		print (stats, bf.split('/')[-1],len(bags),len(pklbags),len(leftpkl))

	print d2s("total_pklbags =", total_pklbags)
	print d2s("total time =", total_pklbags/2. /60.,"hours")