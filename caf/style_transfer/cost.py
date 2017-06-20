from kzpy3.caf.style_transfer import *

class CaffeCost(object):
    __metaclass__ = abc.ABCMeta
    """
    Abstract class for adding in a cost into a caffe back propagation
    assumes that the forward propagation has been called
    """

    def __init__(self, net, layer, w=1.):
        """
        Initializes cost object
        net : caffe network
        weight : float
            Weight associated with this cost
        layer : str
            self.grad specifies dCost/dlayer
        """
        self.net = net
        self.w = w
        self.layer = layer
        self.f0 = net.blobs[layer].data.copy()

    @abc.abstractmethod
    def cost(self):
        """
        (N,)
        """
        pass

    @abc.abstractmethod
    def grad(self):
        """
        (N, K, H, W)
        """
        pass


class StyleCaffeCost(CaffeCost):

    """
    Class to match style of a layer
    """

    def __init__(self, net, layer, w=1.):
        super(StyleCaffeCost, self).__init__(net, layer, w=w)
        self.g0 = self.feature_map_correlation(self.f0)
        _, k, h, W = self.f0.shape
        self.c = 1. / (1. * k * h * W) ** 2

    def cost(self):
        """
        Gives the value of the cost function for current_image

        ----------
        Parameters
        ----------
        current_image : numpy array, shape (N, K, H, W)
            Image whose activations we want to match to
            self.target_activations

        -------
        Returns
        -------
        cost : array, shape (N,)
            Value of the cost function for each image
        """
        f = self.net.blobs[self.layer].data
        g = self.feature_map_correlation(f)

        return (self.w * 0.25 * self.c * ((g - self.g0) ** 2).sum(axis=(1, 2)))

    def grad(self):
        """
        Returns the gradient of the cost function with respect to the input

        ----------
        Parameters
        ----------
        current_image : numpy array, shape (N, K, H, W)
            Image whose activations we want to match to
            self.target_activations

        -------
        Returns
        -------
        grad : array, shape (N, K, H, W)
            Gradient of the cost function with respect to the image
        """
        f = self.net.blobs[self.layer].data
        g = self.feature_map_correlation(f)
        # Trick to get caffe to give us the gradients:
        n, k, h, w = f.shape
        # top_grad = np.einsum('NKk, NkHW -> NKHW', g - self.g0, f)
        top_grad = np.dot((g - self.g0)[0],
                          f[0].reshape(k, -1)).reshape(n, k, h, w)
        # top_grad[f <= 0] = 0.
        return top_grad * self.w * self.c

    def feature_map_correlation(self, fmap):
        """
        Computes the correlation between feature maps

        ----------
        Parameters
        ----------
        fmap : array, shape (N, K, H, W)
            Collection of feature maps

        -------
        Returns
        -------
        corr : array, shape (N, K, K)
            Correlation map between the two feature maps for each image
        """
        # return np.einsum('nkhw, nKhw->nkK', fmap, fmap)
        # FIXME for not n==1
        n, k, h, w = fmap.shape
        return np.dot(fmap[0].reshape(k, -1),
                      fmap[0].reshape(k, -1).transpose()).reshape(1, k, k)


class ContentCaffeCost(CaffeCost):

    """
    Class that wraps what is needed for a term of the cost function
        that matches the activations of a given image to that of an
        image to be found using optimization
    """

    def __init__(self, net, layer, w=1.):
        """
        Initialize the Cost object

        ----------
        Parameters
        ----------
        net : caffe net
            Caffe network to help get derivatives
        target_layer : str
            String indexing which layer this cost corresponds to
        w : float
            Number weighting the influence of this term on the cost function
        """
        super(ContentCaffeCost, self).__init__(net, layer, w=w)
        n, k, h, W = self.f0.shape
        self.c = 1. / (1.0 * h * W)

    def cost(self):
        """
        Gives the value of the cost function for current_image

        ----------
        Parameters
        ----------
        current_image : numpy array, shape (N, K, H, W)
            Image whose activations we want to match to
            self.target_activations

        -------
        Returns
        -------
        cost : array, shape (N,)
            Value of the cost function for each image
        """

        f = self.net.blobs[self.layer].data

        return (self.w * self.c * 0.5 *
                ((f - self.f0) ** 2).sum(axis=(1, 2, 3)))

    def grad(self):
        """
        Returns the gradient of the cost function with respect to the input

        ----------
        Parameters
        ----------
        current_image : numpy array, shape (N, K, H, W)
            Image whose activations we want to match to
            self.target_activations

        -------
        Returns
        -------
        grad : array, shape (N, K, H, W)
            Gradient of the cost function with respect to the image
        """
        f = self.net.blobs[self.layer].data
        # Trick to get caffe to give us the gradients:
        top_grad = f - self.f0
        # top_grad[f <= 0] = 0.
        return top_grad * self.w * self.c


