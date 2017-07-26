from kzpy3.caf.style_transfer.cost import *


class StyleTransfer(object):

    """
    Class for running style transfer
    """

    def __init__(self, net, transformer, args):
        """
        Initialize the Style Transfer object

        ----------
        Parameters
        ----------
        net : caffe._caffe.Net
            Caffe network
        transformer : caffe.io.Transformer
            Transformer that takes in images and prepares them to be
            added to the data layer
        args : argparse.Namespace
            Result from commandline argument parsing
        """
        self.net = net
        self.transformer = transformer
        self.args = args

        # Load Images and Reshape Caffe input to content image
        '''
        self.raw_style_img = caffe.io.load_image('/Users/karlzipser/Desktop/cat_360.jpg')#npsq2_512.jpg')#'/Users/karlzipser/Desktop/starry_night_sq.jpg')#opjh('Pictures/bay2.png'))#caffe.io.load_image('/Users/karlzipser/caffe/examples/images/cat.jpg')#
            #os.path.join(args.data_folder, args.style_file))
        self.raw_content_img = caffe.io.load_image('/Users/karlzipser/Desktop/cat_360.jpg')#npsq2_512.jpg')#np.random.random((512,512,3)) #imresize(caffe.io.load_image('/Users/karlzipser/Desktop/npsq2.jpg'),(512,512,3))#np.random.random((4*256,4*256,3))#+0.5*imresize(caffe.io.load_image('/Users/karlzipser/Desktop/npsq2lr.jpg'),[256,256,3]) #np.random.random((256,256,3))#imresize(caffe.io.load_image('/Users/karlzipser/Desktop/david-full-front.jpg'),100)#opjh('Pictures/bay2.png')),25)
        #np.random.random((141,250,3)) #(324, 484,3)) #np.shape(self.raw_style_img))# (256,256,3))#(1296, 1936,3))#caffe.io.load_image('/Users/karlzipser/caffe/examples/images/cat.jpg')#caffe.io.load_image(
            #os.path.join(args.data_folder, args.content_file))
        '''
        self.raw_style_img = caffe.io.load_image(os.path.join(args.data_folder, args.style_file))
        self.raw_content_img = caffe.io.load_image(os.path.join(args.data_folder, args.content_file))

        h, w, k = self.raw_content_img.shape
        print 'The dimensions of the content image is ' + str((h, w))
        net.blobs['data'].reshape(1, k, h, w)
        transformer.inputs['data'] = (1, k, h, w)

        style_img = transformer.preprocess('data', self.raw_style_img)
        content_img = transformer.preprocess('data', self.raw_content_img)

        # Layers and weights
        if args.network == 'vgg':
            style_ls = ['conv1_1',
                        'conv2_1',
                        'conv3_1',
                        'conv4_1']
            style_ws = [0.2 * args.sc_ratio] * 5
            content_ls = ['conv5_1','conv5_2','conv5_3','conv5_4']
            content_ws = [1.0]
        elif args.network == 'bvlc_reference_caffenet':
            style_ls = ['conv1',
                        'conv2',
                        'conv3',
                        'conv4',
                        'conv5']
            style_ws = [0.2 * args.sc_ratio] * 5
            content_ls = ['conv4','conv5']
            content_ws = [1.0]
        elif args.network == 'bvlc_googlenet':
            style_ls = ["conv1/7x7_s2",
                        "conv2/3x3",
                        "inception_3a/1x1",
                        "inception_3b/1x1",
                        "inception_4a/1x1",
                        "inception_4b/1x1",
                        "inception_4c/1x1",
                        "inception_4d/1x1"]
            style_ws = [0.2 * args.sc_ratio] * 5
            content_ls = ["inception_5b/1x1","inception_5b/3x3","inception_5b/5x5"]#"inception_3a/3x3","inception_3b/3x3","inception_3c/3x3"]
            content_ws = [1.0]
        else:
            raise ValueError('Invalid Network')

        # Prepare list of costs based off of caffe layers
        caffe_costs = []

        # Build Style Costs
        net.blobs['data'].data[0] = style_img
        net.forward()
        caffe_costs = []
        for l, w in zip(style_ls, style_ws):
            caffe_costs.append(StyleCaffeCost(net, l, w))

        # Build Content Costs
        net.blobs['data'].data[0] = content_img
        net.forward()
        for l, w in zip(content_ls, content_ws):
            caffe_costs.append(ContentCaffeCost(net, l, w))

        self.caffe_costs = caffe_costs
        for lr in net.blobs.keys():
            net.blobs[lr].data[:] = 0.
            net.blobs[lr].diff[:] = 0.

        # Form list of costs acting on the input
        self.input_costs = []  # [TotalVariationCost(6, w = ??)]

        # Form a list of unique layers in reverse order for backprop
        idx = []
        lrs = net.blobs.keys()
        for cost in caffe_costs:
            idx.append(lrs.index(cost.layer))
        un = np.unique(np.array(idx))
        un.sort()
        self.lrs = [lrs[ix] for ix in un]
        self.lrs.reverse()

    def cost(self, img, verbose=False):
        """
        Computes the value of the style and content cost function for img

        ----------
        Parameters
        ----------
        img : array, shape (1, K, H, W)
            Imaged processed by self.transformer
        verbose : bool
            If true, output each subcost individually

        -------
        Returns
        -------
        tot : array, shape (1,)
            Value of cost for img

        costs : list of array, shape (1,)
            OPTIONAL: list of costs for each subcost
        """
        self.net.blobs['data'].data[:] = img
        self.net.forward()
        tot = np.zeros((img.shape[0],)).astype('float64')
        subcosts = []
        for cost in self.caffe_costs:
            v = cost.cost()
            subcosts.append((cost.layer, v[0]))
            tot += v
        for cost in self.input_costs:
            v = cost.cost()
            subcosts.append(('input', v[0]))
            tot += v
        if verbose:
            tot = tot, subcosts
        return tot

    def grad(self, img):
        """
        Returns the gradient of the content and style cost function for img

        ----------
        Parameters
        ----------
        img : array, shape (1, K, H, W)
            Image to get the cost of

        -------
        Returns
        -------
        diff : array, shape (1, K, H, W)
            Gradient of cost with respect to img
        """
        self.net.blobs['data'].data[:] = img
        self.net.forward()
        self.net.blobs[self.lrs[-1]].diff[:] = 0.
        # Backpropagate through layers
        for lr, nxt_lr in zip(self.lrs, self.lrs[1:] + [None]):
            grad = self.net.blobs[lr].diff
            for cost in self.caffe_costs:
                if cost.layer == lr:
                    grad += cost.grad()
            self.net.backward(start=lr, end=nxt_lr)

        grad = self.net.blobs['data'].diff.astype('float64')
        for cost in self.input_costs:
            grad += cost.grad(img)
        return grad




    '''
        src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
        net.forward(end=end)

        objective(dst)  # specify the optimization objective
        net.backward(start=end)
        g = src.diff[0]
        # apply normalized ascent step to the input image
        
        denom = np.abs(g).mean()
        if denom:
            src.data[:] += step_size/denom * g
        else:
            print(d2s('Warnging: denom =',denom))
            return False
        
        src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
    '''



    def lbfgs_cost_optimizer(self):
        """
        Calls lbfgs optimizer to minimize the cost function
        """
        x0 = self.transformer.preprocess(
            'data', np.random.random(np.shape(self.raw_content_img)),#self.raw_content_img
            ).copy()[np.newaxis, :]
        n, k, h, w = x0.shape

        pb = ProgressBar(self.args.n_itr)
        self.it_count = 0
        self.imgpath = opjh(d2n('Desktop/',np.int(time.time()),'.png'))

        def f(x):
            #jitter = 1
            #ox, oy = np.random.randint(-jitter, jitter+1, 2)
            self.it_count += 1
            pb.animate(self.it_count)
            #y = reshape(x,(360,360,3))
            #y = np.roll(np.roll(y, ox, -1), oy, -2)
            x = x.reshape(n, k, h, w)

            #x = 200*z2o(zscore(x,2.5))-100

            self.save_image(x,self.imgpath)
            
            return self.cost(x).ravel()

        def fp(x):
            x = x.reshape(n, k, h, w)
            return self.grad(x).ravel()

        # mm = self.transformer.
        bnds = [(-104, 130) for _ in x0.ravel()]
        print 'Optimization starting'
        start = timeit.default_timer()
        out = fmin_l_bfgs_b(f, x0.flatten(), fprime=fp, maxfun=self.args.n_itr, bounds=bnds, factr = 0)
        #out = fmin_l_bfgs_b(f, x.flatten(), fprime=fp, maxfun=self.args.n_itr, bounds=bnds, factr = 0)
        #ox,oy = 0,0
        for i in range(self.args.n_itr):
            x = out[0].reshape(n, k, h, w)
            #jitter = 0#14
            #y = reshape(x,(360,360,3))
            #y = np.roll(np.roll(y, -ox, -1), -oy, -2)
            #ox, oy = np.random.randint(-jitter, jitter+1, 2)
            #y = np.roll(np.roll(y, ox, -1), oy, -2)
            #x = y.reshape(n, k, h, w)
            out = fmin_l_bfgs_b(f, x.flatten(), fprime=fp, maxfun=1, bounds=bnds, factr = 0)

        end = timeit.default_timer()
        print("Took {0:.0f} seconds".format(end - start))

        x = out[0].reshape(n, k, h, w)

        _, subcosts = self.cost(x, verbose=True)
        for sc in subcosts:
            print sc
        return x, out

    def save_image(self, x, fn):
        """
        Saves the image produced by lbfgs

        ----------
        Parameters
        ----------
        x : array, shape (1, K, H, W)
            Image in caffe network input format to be saved
        """
        img = self.transformer.deprocess('data', x[0])
        # img = caffe.io.resize_image(img, self.raw_content_img.shape,
        #                             interp_order=3)
        img = np.clip(img, 0., 1.)
        img = (255 * img).astype('uint8')
        imsave(os.path.join(self.args.output_dir, fn), img)


