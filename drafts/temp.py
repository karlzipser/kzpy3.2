#,a
if False:
	CA()
	if 'D' in locals():
		try_to_close(D)
	D = h5r(opjD('Depth_images','tegra-ubuntu_01Nov18_13h09m32s.Depth_image.h5py'))


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
	image[:,:,2] = a
	mci(image,scale=3.0)
	time.sleep(0.25)
#,b