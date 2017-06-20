# These examples are from various files distributed with caffe

from kzpy3.utils import *
import caffe




class SimpleLayer0(caffe.Layer):
    """A layer that just multiplies by one."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
        top[0].data[...] = 1.0 * bottom[0].data

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff


class SimpleLayer1(caffe.Layer):
    """A layer that sometimes reverses contrast."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
    	r = np.random.random()
    	#print(r)
    	if r < 0.5:
        	top[0].data[...] = bottom[0].data - 0.5
        else:
        	top[0].data[...] = 1.0 - bottom[0].data - 0.5

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer2(caffe.Layer):
    """A layer that adds distractors."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        tp = zeros((1,1,28,28))
        n = 12
        n2 = 10
        for i in range(100):
            top[0].data[i,:,:,:] = bottom[0].data[i,:,:,:] - 0.5
            mx = top[0].data[i,:,:,:].max()
            top[0].data[i,:,:,:n] += bottom[0].data[randint(100),:,:,-n:]
            top[0].data[i,:,:,-n:] += bottom[0].data[randint(100),:,:,:n]
            top[0].data[i,:,:n2,:] += bottom[0].data[randint(100),:,-n2:,:]
            top[0].data[i,:,-n2:,:] += bottom[0].data[randint(100),:,:n2,:]
            tp = top[0].data[i,:,:,:]
            tp[tp>mx] = mx


            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer


class SimpleLayer3(caffe.Layer):
    """A layer that addds distractcors, sometimes reverses contrast."""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)
    
    def forward(self, bottom, top):
        tp = zeros((1,1,28,28))
        n = 12
        n2 = 10
        for i in range(100):
            top[0].data[i,:,:,:] = bottom[0].data[i,:,:,:] - 0.5
            mx = top[0].data[i,:,:,:].max()
            top[0].data[i,:,:,:n] += bottom[0].data[randint(100),:,:,-n:]
            top[0].data[i,:,:,-n:] += bottom[0].data[randint(100),:,:,:n]
            top[0].data[i,:,:n2,:] += bottom[0].data[randint(100),:,-n2:,:]
            top[0].data[i,:,-n2:,:] += bottom[0].data[randint(100),:,:n2,:]
            tp = top[0].data[i,:,:,:]
            tp[tp>mx] = mx
            if np.random.random(1)[0] > 0.5:
                top[0].data[i,:,:,:] = mx-tp

            #top[0].data[i,:,:,:] += np.random.random(shape(bottom[0].data[r,:,:,:]))
    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 1.0 * top[0].diff # don't know what this should be, but perhaps it doesn't matter for a data layer



