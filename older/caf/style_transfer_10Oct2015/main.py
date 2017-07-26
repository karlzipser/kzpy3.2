from kzpy3.caf.style_transfer.stran import *

"""
python ~/kzpy3/caf/style_transfer/main.py

"""

def build_net(model_path, net_fn, param_fn, args, data_mean=None):
    """
    Loads an imagenet classifier, building the net and transformer

    ----------
    Parameters
    ----------
    model_path : str
        Path where the model is saved
    net_fun : str
        Filename of 'deploy.prototxt' for the model, containing
        the definition of the model architecture
    param_fun : str
        Filename of parameter file, usually ends in '.caffemodel'
    scale : int
        Scale the size of the input by scale
    data_mean : array, shape (3,)
        Mean for each color (defaults to imgenet means)

    -------
    Returns
    -------
    net: caffe net
        Caffe network object
    transformer: caffe Transformer
        Transformer that takes in HWK images and puts them into the
        appropriate format for the caffe model
        see: https://github.com/BVLC/caffe/blob/master/python/caffe/io.py
    """
    # scale = args.img_scale
    caffe_root = args.caffe_root
    net_fn = os.path.join(model_path, net_fn)
    param_fn = os.path.join(model_path, param_fn)
    if data_mean is None:
        mean_path = os.path.join(caffe_root, "python", "caffe", "imagenet",
                                 "ilsvrc_2012_mean.npy")
        data_mean = np.load(mean_path).mean((1, 2))

    net = caffe.Net(net_fn, param_fn, caffe.TEST)

    _, k, h, w = net.blobs['data'].data.shape
    net.blobs['data'].reshape(1, k, h, w)  # Only one image

    # Input preprocessing
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))  # HWK to KHW
    transformer.set_mean('data', data_mean)  # color channel means
    transformer.set_raw_scale('data', 255)  # Scale for network input
    transformer.set_channel_swap('data', (2, 1, 0))  # BGR instead of RGB

    return net, transformer





def fn_gen(d, ext='jpg'):
    """
    Helper method to generate filenames

    Parameters
    ----------
    d : dict
        Dictionary giving options and their values to be converted to a string
    ext : str
        Extension for filename

    Returns
    -------
    fn : str
        Filename with options
    """
    fn = ''
    for i, k in enumerate(d.keys()):
        if i > 0:
            fn += '__'
        fn += str(k) + '_' + str(d[k])
    fn = fn.replace('.', "")
    return fn + '.' + ext
    
"""
bvlc_googlenet
bvlc_googlenet.caffemodel
deploy_headless.prototxt
style_ls = [
    "conv1/7x7_s2",
    "conv2/3x3",
    "inception_3a/1x1",
    "inception_3b/1x1",
    "inception_4a/1x1",
    "inception_4b/1x1",
    "inception_4c/1x1",
    "inception_4d/1x1"]
style_ws = [0.2 * args.sc_ratio] * 5
content_ls = [
    "inception_5b/1x1",
    "inception_5b/3x3",
    "inception_5b/5x5"]
content_ws = [1.0]
content_file = opjh('Desktop/cat.jpg')
style_file = opjh('Desktop/cat.jpg')
sc_ratio
"""

if __name__ == '__main__':
    parser = ArgumentParser('Invert a sum of layer matching costs. Karl version.\n')

    parser_info = [
        ['--gpu',           int,    -1,                         "Index of gpu, gpu=-1"],
        ['--network',       str,    'vgg',           "Name of network, vgg or bvlc_googlenet or bvlc_reference_caffenet"],#'',
        ['--caffe_root',    str,    'laptop',                   'caffe_root, if computer or cluster, do nothing'],
        ['--n_itr',         int,    10000,                      'Number of iterations to run descent'],
        ['--data_folder',   str,    opjh('Desktop'),            'Folder containing the data'],
        ['--output_dir',    str,    opjh('Desktop'),            'Directory to save images'],
        ['--content_file',  str,    opjh('Desktop/cat.jpg'),    'Filename for content image'],
        ['--style_file',    str,    opjh('Desktop/cat.jpg'),  'Filename for style image'],
        ['--sc_ratio',      float,  1.,                         'Ratio of style weight to content weight'],
        ['--img_scale',     int,    1,                          'Ratio to scale size of input. Try 1 or 2']]

    for p_i in parser_info:
        parser.add_argument(p_i[0], type=p_i[1], default=p_i[2],help=p_i[2])

    args = parser.parse_args()
    args.caffe_root = opjh('caffe')

    print 'The network is ' + args.network
    if args.network == 'vgg':
        model_folder = 'models/VGG_ILSVRC_19_layers'
        net_fn = 'deploy_headless.prototxt'
        # param_fn = 'vgg_normalised.caffemodel'
        param_fn = 'VGG_ILSVRC_19_layers.caffemodel'
    elif args.network == 'bvlc_googlenet':
        model_folder = 'models/bvlc_googlenet'
        net_fn = 'deploy_headless.prototxt'
        param_fn = 'bvlc_googlenet.caffemodel'
    elif args.network == 'bvlc_reference_caffenet':
        model_folder = 'models/bvlc_reference_caffenet'
        net_fn = 'deploy_headless.prototxt'
        param_fn = 'bvlc_reference_caffenet.caffemodel'
    else:
        raise ValueError('Unrecognized network')
    model_path = os.path.join(args.caffe_root, model_folder)

    if args.gpu >= 0:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu)
    elif args.gpu == -1:
        caffe.set_mode_cpu()
    else:
        raise ValueError('Unrecognized gpu mode')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    net, transformer = build_net(
        model_path, net_fn, param_fn, args)

    st = StyleTransfer(net, transformer, args)
    x, _ = st.lbfgs_cost_optimizer()
    fn = fn_gen({'content': args.content_file.replace('.jpg', ''),
                 'ratio_x100': int(args.sc_ratio * 100),
                 'style': args.style_file.replace('.jpg', '')})
    st.save_image(x, fn)
