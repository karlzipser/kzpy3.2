net = caffe.Classifier(
	'/Users/karlzipser/Google_Drive/models_caffe/nin_imagenet_conv_sandbox/deploy.prototxt',
	'/Users/karlzipser/Google_Drive/models_caffe/nin_imagenet_conv_sandbox/model.caffemodel',
	mean = np.float32([104.0, 116.0, 122.0]),
	channel_swap = (2,1,0))


for l in [(k, v.data.shape) for k, v in net.blobs.items()]:
    print l

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(opj(home_path,'caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

net.blobs['data'].reshape(1,3,224,224)



plt.plot(net.blobs['pool4'].data[0,:,0,0])




def my_scatter(x,y,xmin,xmax,fig_wid,fig_name):
	plt.figure(fig_name,(fig_wid,fig_wid))
	plt.clf()
	plt.plot(x,y,'bo')
	plt.title(np.corrcoef(x,y)[0,1])
	plt.xlim(xmin,xmax)
	plt.ylim(xmin,xmax)


###########


n = 10000
xs_target = []
ys_target = []
xs_out = []
ys_out = []

for i in range(n):
	solver.net.forward()
	xs_target.append(solver.net.blobs['py_target_data'].data[0,0])
	ys_target.append(solver.net.blobs['py_target_data'].data[0,1])
	xs_out.append(solver.net.blobs['ip2'].data[0,0])
	ys_out.append(solver.net.blobs['ip2'].data[0,1])
plt.figure('xs',(5,5))
plt.clf()
plt.plot(xs_target,xs_out,'bo');plt.title(np.corrcoef(xs_target,xs_out)[0,1])
plt.xlim(0,1)
plt.ylim(0,1)
plt.figure('ys',(5,5))
plt.clf()
plt.plot(ys_target,ys_out,'ro');plt.title(np.corrcoef(ys_target,ys_out)[0,1])
plt.xlim(0,1)
plt.ylim(0,1)


# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0):
	data -= data.min()
	data /= data.max()

	# force the number of filters to be square
	n = int(np.ceil(np.sqrt(data.shape[0])))
	padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
	data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

	# tile the filters into an image
	data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
	data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

	plt.imshow(data)

def my_vis_square(data, padsize=5, padval=0):
	data = data.copy()
	data = z2o(data)
	n = int(np.ceil(np.sqrt(data.shape[0])))
	fx = np.shape(data)[2]
	fz = np.shape(data)[1]
	img = np.zeros((padsize+(padsize+fx)*n,padsize+(padsize+fx)*n))+padval
	for x in range(n):
		for y in range(n):
			if y+x*n < data.shape[0]:
				img[(padsize*(1+x)+(x*(fx))):(padsize*(1+x)+((x+1)*fx)),(padsize*(1+y)+(y*fx)):(padsize*(1+y)+((y+1)*fx))] = data[y+x*n,0,:,:]
	mi(img,2)




