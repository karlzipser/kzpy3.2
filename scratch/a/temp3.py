

def get_color_frame(i):
	f = zeros((224,298,3),'uint8')
	for j in range(3):
		f[:,:,j] = imread(opjh('scratch/2015/11/23/RPi_frames0',d2n(i+j,'.jpeg')))
	return f

for i in range(0,5531,3):
	imsave(opjh('scratch/2015/11/23/RPi_colored_frames',d2n(i,'.jpeg')),get_color_frame(i))

	