#,a
if True:#'D' not in locals():
	#CA()
	#if 'D' in locals():
	#	try_to_close(D)
	run_name = 'tegra-ubuntu_01Nov18_13h09m32s.Depth_image.h5py'
	#run_name = 'tegra-ubuntu_30Oct18_15h58m09s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_15Nov18_20h52m26s.Depth_image.h5py'
	run_name = 'tegra-ubuntu_01Nov18_13h09m32s.Depth_image.h5py'
	D = h5r(opjD('Depth_images',run_name
		))
		


image = zeros((32,360,3),np.uint8)
images = []
for i in range(shape(D['depth'])[0]):
	a = D['depth'][i,:,:]/5.0*255
	a[a>255] = 255
	a[a<0] = 0
	image[:,:,0] = 255-a

	a = D['camera'][i,:,:]
	#print a.max(),a.min()
	#b = a.flatten()
	#hist(b);spause()
	a = a/300.0*255
	a[a>255] = 255
	a[a<0] = 0
	image[:,:,1] = a

	a = D['other'][i,:,:]
	
	a = a/500.0*255
	#a[a<500] = 500
	#a[a>5000] = 5000
	#a = 255 * (a-500) / 4500.
	a[a>255] = 255
	a[a<0] = 0
	a = 255-a
	#image[:,:,2] = a
	mci(image,scale=3.0,title=run_name)
	time.sleep(0.25)
#,b