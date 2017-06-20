# These examples are from various files distributed with caffe

import caffe
import numpy as np


class EuclideanLossLayer(caffe.Layer):
    """
    Compute the Euclidean Loss in the same manner as the C++ EuclideanLossLayer
    to demonstrate the class interface for developing layers in Python.
    """

    def setup(self, bottom, top):
        # check input pair
        if len(bottom) != 2:
            raise Exception("Need two inputs to compute distance.")

    def reshape(self, bottom, top):
        # check input dimensions match
        if bottom[0].count != bottom[1].count:
            raise Exception("Inputs must have the same dimension.")
        # difference is shape of inputs
        self.diff = np.zeros_like(bottom[0].data, dtype=np.float32)
        # loss output is scalar
        top[0].reshape(1)

    def forward(self, bottom, top):
        self.diff[...] = bottom[0].data - bottom[1].data
        top[0].data[...] = np.sum(self.diff**2) / bottom[0].num / 2.

    def backward(self, top, propagate_down, bottom):
        for i in range(2):
            if not propagate_down[i]:
                continue
            if i == 0:
                sign = 1
            else:
                sign = -1
            bottom[i].diff[...] = sign * self.diff / bottom[i].num

class SimpleLayer(caffe.Layer):
    """A layer that just multiplies by ten"""

    def setup(self, bottom, top):
        pass

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
        top[0].data[...] = 10 * bottom[0].data

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = 10 * top[0].diff


class ExceptionLayer(caffe.Layer):
    """A layer for checking exceptions from Python"""

    def setup(self, bottom, top):
        raise RuntimeError


"""name: 'pythonnet' force_backward: true
        input: 'data' input_shape { dim: 10 dim: 9 dim: 8 }
        layer { type: 'Python' name: 'one' bottom: 'data' top: 'one'
          python_param { module: 'layer_examples' layer: 'SimpleLayer' } }
        layer { type: 'Python' name: 'two' bottom: 'one' top: 'two'
          python_param { module: 'layer_examples' layer: 'SimpleLayer' } }
        layer { type: 'Python' name: 'three' bottom: 'two' top: 'three'
          python_param { module: 'layer_examples' layer: 'SimpleLayer' } }"""



class SimpleParamLayer(caffe.Layer):
    """A layer that just multiplies by the numeric value of its param string"""

    def setup(self, bottom, top):
        try:
            self.value = float(self.param_str)
        except ValueError:
            raise ValueError("Parameter string must be a legible float")

    def reshape(self, bottom, top):
        top[0].reshape(*bottom[0].data.shape)

    def forward(self, bottom, top):
        top[0].data[...] = self.value * bottom[0].data

    def backward(self, top, propagate_down, bottom):
        bottom[0].diff[...] = self.value * top[0].diff

"""name: 'pythonnet' force_backward: true
        input: 'data' input_shape { dim: 10 dim: 9 dim: 8 }
        layer { type: 'Python' name: 'mul10' bottom: 'data' top: 'mul10'
          python_param { module: 'layer_examples'
                layer: 'SimpleParamLayer' param_str: '10' } }
        layer { type: 'Python' name: 'mul2' bottom: 'mul10' top: 'mul2'
          python_param { module: 'layer_examples'
                layer: 'SimpleParamLayer' param_str: '2' } }"""


