from kzpy3.utils import *


def first_iso_layer(layer_num,in_bottom,num_hid,num_out):
	iso_conv_layer = '''

	layer {
	  name: "icLAYER_hid"
	  type: "Convolution"
	  IN_BOTTOM
	  top: "icLAYER_hid"
	  convolution_param {
	    num_output: NUM_HID
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid"
	  top: "icLAYER_hid"
	}
	layer {
	  name: "icLAYER_out"
	  type: "Convolution"
	  bottom: "icLAYER_hid"
	  top: "icLAYER_out"
	  convolution_param {
	    num_output: NUM_OUT
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out"
	  top: "icLAYER_out"
	}
	'''

	iso_conv_layer = iso_conv_layer.replace('LAYER',str(layer_num))
	iso_conv_layer = iso_conv_layer.replace('IN_BOTTOM',in_bottom)
	iso_conv_layer = iso_conv_layer.replace('NUM_HID',str(num_hid))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT',str(num_out))

	return iso_conv_layer



def iso_layer(layer_num,in_bottom,num_hid,num_out):
	iso_conv_layer = '''
	layer {
	  name: "icLAYER_in"
	  type: "Concat"
	  IN_BOTTOM
	  top: "icLAYER_in"
	}
	layer {
	  name: "icLAYER_hid"
	  type: "Convolution"
	  bottom: "icLAYER_in"
	  top: "icLAYER_hid"
	  convolution_param {
	    num_output: NUM_HID
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid"
	  top: "icLAYER_hid"
	}
	layer {
	  name: "icLAYER_out"
	  type: "Convolution"
	  bottom: "icLAYER_hid"
	  top: "icLAYER_out"
	  convolution_param {
	    num_output: NUM_OUT
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out"
	  top: "icLAYER_out"
	}
	'''

	iso_conv_layer = iso_conv_layer.replace('LAYER',str(layer_num))
	iso_conv_layer = iso_conv_layer.replace('IN_BOTTOM',in_bottom)
	iso_conv_layer = iso_conv_layer.replace('NUM_HID',str(num_hid))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT',str(num_out))

	return iso_conv_layer

layers_dic = {}


layer_num = 0
layers_dic[layer_num] = '''layer {
  name: "data"
  type: "Data"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  transform_param {
    scale: 0.00392156862745
  }
  data_param {
    source: "caffe/data/mnist/mnist_train_lmdb"
    batch_size: 100
    backend: LMDB
  }
}
layer {
  name: "data"
  type: "Data"
  top: "data"
  top: "label"
  include {
    phase: TEST
  }
  transform_param {
    scale: 0.00392156862745
  }
  data_param {
    source: "caffe/data/mnist/mnist_test_lmdb"
    batch_size: 100
    backend: LMDB
  }
}
layer {
  type: 'Python'
  name: 'pydata'
  bottom: 'data'
  top: 'pydata'
  python_param {
    module: 'kz_layers0'
    layer: 'SimpleLayer2'
  }
  include {
    phase: TRAIN
  }
}
layer {
  type: 'Python'
  name: 'pydata'
  bottom: 'data'
  top: 'pydata'
  python_param {
    module: 'kz_layers0'
    layer: 'SimpleLayer2'
  }
  include {
    phase: TEST
  }
}
'''




layer_num = 1
in_bottom = '''	bottom: 'pydata' '''
num_hid = 20
num_out = 3
layers_dic[layer_num] = first_iso_layer(layer_num,in_bottom,num_hid,num_out)

layer_num = 2
in_bottom = '''	bottom: 'ic1_hid'
  		bottom: 'ic1_out' '''
layers_dic[layer_num] = iso_layer(layer_num,in_bottom,num_hid,num_out)

layer_num = 3
in_bottom = '''	bottom: 'ic1_out'
  		bottom: 'ic2_hid'
  		bottom: 'ic2_out' '''
layers_dic[layer_num] = iso_layer(layer_num,in_bottom,num_hid,num_out)


for layer_num in range(4,17):
	in_bottom = '''	bottom: 'ic111_out'
  		bottom: 'ic222_out'
  		bottom: 'ic333_hid'
  		bottom: 'ic333_out' '''
  	in_bottom = in_bottom.replace('111',str(layer_num-3))
  	in_bottom = in_bottom.replace('222',str(layer_num-2))
  	in_bottom = in_bottom.replace('333',str(layer_num-1))
	layers_dic[layer_num] = iso_layer(layer_num,in_bottom,num_hid,num_out)

top_layers = '''
layer {
  name: "ip"
  type: "InnerProduct"
  bottom: "BOTTOM"
  top: "ip"
  inner_product_param {
    num_output: 10
    weight_filler {
      type: "xavier"
    }
  }
}
layer {
  name: "accuracy"
  type: "Accuracy"
  bottom: "ip"
  bottom: "label"
  top: "accuracy"
  include {
    phase: TEST
  }
}
layer {
  name: "loss"
  type: "SoftmaxWithLoss"
  bottom: "ip"
  bottom: "label"
  top: "loss"
}
'''.replace('BOTTOM',d2n('ic',layer_num,'_out'))
layer_num += 1
layers_dic[layer_num] = top_layers


proto_str_lst = []
for i in range(layer_num+1):
	proto_str_lst.append(d2s('#### layer', i, '####'))
	proto_str_lst.append(layers_dic[i])

print('\n'.join(proto_str_lst))
list_of_strings_to_txt_file(opjh('Desktop/train_val.prototxt'),proto_str_lst)
	
