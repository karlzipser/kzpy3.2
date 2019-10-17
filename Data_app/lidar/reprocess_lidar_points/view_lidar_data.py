#,a

if 'D' not in locals():
	#CA()
	#if 'D' in locals():
	#	try_to_close(D)
	run_name = 'tegra-ubuntu_01Nov18_13h09m32s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_30Oct18_15h58m09s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_15Nov18_20h52m26s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_01Nov18_13h09m32s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_01Nov18_13h46m55s.Depth_image.with_left_ts.h5py'
	D = h5r(opjD('Depth_images_copy',run_name))
		

def process_images_to_rgb_v1(D,show=False):
	image = zeros((32,360,3),np.uint8)
	
	Rgb_v1 = {'rgb_v1_normal':[],'rgb_v1_flip':[]}

	for i in range(shape(D['depth'])[0]):

		a = D['depth'][i,:,:]/2.0*255
		a[a>255] = 255
		a[a<0] = 0
		image[:,:,0] = 255-a

		a = D['camera'][i,:,:]
		if False:
			b = a.flatten()
			hist(b);spause()
		a = a/300.0*255
		a[a>255] = 255
		a[a<0] = 0
		image[:,:,1] = a

		a = D['other'][i,:,:]
		a = a/100.0*255
		a[a>255] = 255
		a[a<0] = 0
		a = 255-a
		image[:,:,2] = a

		image_resized = cv2.resize(image,(690,64),interpolation=0)

		image_resized_flip = cv2.flip(image_resized,1)

		Rgb_v1['rgb_v1_normal'].append(image_resized)
		Rgb_v1['rgb_v1_flip'].append(image_resized_flip)

		if show:
			mci(image_resized,scale=2.0,title=run_name,delay=33)

	return Rgb_v1



R = process_images_to_rgb_v1(D)

for i in rlen(R['rgb_v1_normal']):
	img = R['rgb_v1_normal'][i]
	mci(img[:,690/8:-690/8,:],scale=2.0,title=run_name,delay=1)
#,b