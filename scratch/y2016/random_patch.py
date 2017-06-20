from kzpy3.vis import *
plt.ion()
img = imread('/Users/karlzipser/Desktop/2.jpg')
img2 = img.copy()
img_shape = shape(img)

patch_width = int(img_shape[1]/4.0)

x1x2y1y2_lst = []

for x1 in range(img_shape[1]-patch_width):
	for y1 in range(img_shape[0]-patch_width):
		x2 = x1+patch_width
		y2 = y1+patch_width
		assert(x1>=0 and x1<=img_shape[1]-patch_width)
		assert(y1>=0 and y1<=img_shape[0]-patch_width)
		assert(x2<=img_shape[1])
		assert(y2<=img_shape[0])
		print(x1,x2,y1,y2)
		x1x2y1y2_lst.append((x1,x2,y1,y2))

for i in range(len(x1x2y1y2_lst)):
	j = np.random.randint(len(x1x2y1y2_lst))
	(x1,x2,y1,y2) = x1x2y1y2_lst[j]
	mi(img2[y1:y2,x1:x2],2)
	plt.pause(0.5)
	img[y1:y2,x1:x2] *= 0.8
	mi(img)
	plt.pause(0.00000001)



