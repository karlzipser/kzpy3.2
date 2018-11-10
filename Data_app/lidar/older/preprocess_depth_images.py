
from kzpy3.vis3 import *

depth_image_files = sggo(opjD('Depth_images','*.Depth_image.h5py'))

for depth_image_file in depth_image_files:
	cs(depth_image_file)
	error_file = depth_image_file+'.error'
	touched_file = depth_image_file+'.work_in_progress'
	if len(sggo(touched_file)) > 0:
		print(sggo(touched_file))
		cs(depth_image_file,'alread touched.')
		continue
	if len(sggo(error_file)) > 0:
		print(sggo(error_file))
		cs(depth_image_file,'has error.')
		continue
		
	os.system(d2s('touch',touched_file))
	log_min,log_max = -0.25,1.5

	try:
		D=h5rw(depth_image_file)
		r=D['real'][:]
		pa = Progress_animator(len(r),message='r')

		display = False
		r[:,28,:] = r[:,27,:]
		r[:,29,:] = r[:,30,:]

		g = zeros((33,120))
		z = zeros((32,120))
		e = r[0,:,:]

		processed_depth_images = []

		display_timer = Timer(2)

		clear_screen()
		cs("Processing",depth_image_file)
		for i in rlen(r):

			pa['update'](i)

			if i > 0:
				a=r[i,:,:]
				b = a==0.0
				c = b.astype(int)
				d = (1-c)*a + c*e
				e = d.copy()
				f = np.log10(d+.001)
				h = (f>log_max).astype(int)
				k = (1-h)*f + h*(z+log_max)
				h = (f<log_min).astype(int)
				k = (1-h)*k + h*(z+log_min)
				if i == 1:
					processed_depth_images.append(k)
					# since first image has no previous, make first image equal second
				processed_depth_images.append(k)
				if display_timer.check():
					g[:32,:] = k
					g[32,0] = 1.5
					g[32,1:] = -0.25
					mi(1-g,fname(depth_image_file))
					if False:
						figure('hist');clf()
						hist(d.flatten(),bins=100);xylim(0,100,0,200)
						figure('log10 hist');clf()
						hist(k.flatten(),bins=100);xylim(-2,2,0,200)
					display_timer.reset()
			spause()
		assert len(processed_depth_images) == len(D['index'][:])
		D.create_dataset('log',data=na(processed_depth_images))
		D.close()
		os.system('rm '+touched_file)
		os.system(d2s('mv',depth_image_file,depth_image_file.replace('image.','images.')))
		
	except Exception as e:
		os.system('rm '+touched_file)
		os.system('touch '+error_file)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',emphasis=True)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

cs('Done.')


#EOF