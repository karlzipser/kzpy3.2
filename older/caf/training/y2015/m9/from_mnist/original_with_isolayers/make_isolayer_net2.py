from kzpy3.utils import *


def iso_layer(layer_num,in_bottom,num_hid1,num_hid2,num_out1,num_out2):
	iso_conv_layer = '''
	layer {
	  name: "icLAYER_in"
	  type: "Concat"
	  IN_BOTTOM
	  top: "icLAYER_in"
	}
	layer {
	  name: "icLAYER_hid1"
	  type: "Convolution"
	  bottom: "icLAYER_in"
	  top: "icLAYER_hid1"
	  convolution_param {
	    num_output: NUM_HID1
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid1_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid1"
	  top: "icLAYER_hid1"
	}	
	layer {
	  name: "icLAYER_hid2"
	  type: "Convolution"
	  bottom: "icLAYER_hid1"
	  top: "icLAYER_hid2"
	  convolution_param {
	    num_output: NUM_HID2
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid2_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid2"
	  top: "icLAYER_hid2"
	}
	layer {
	  name: "icLAYER_out1"
	  type: "Convolution"
	  bottom: "icLAYER_hid2"
	  top: "icLAYER_out1"
	  convolution_param {
	    num_output: NUM_OUT1
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out1_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out1"
	  top: "icLAYER_out1"
	}
	layer {
	  name: "icLAYER_out2"
	  type: "Convolution"
	  bottom: "icLAYER_out1"
	  top: "icLAYER_out2"
	  convolution_param {
	    num_output: NUM_OUT2
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out2_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out2"
	  top: "icLAYER_out2"
	}
	'''

	iso_conv_layer = iso_conv_layer.replace('LAYER',str(layer_num))
	iso_conv_layer = iso_conv_layer.replace('IN_BOTTOM',in_bottom)
	iso_conv_layer = iso_conv_layer.replace('NUM_HID1',str(num_hid1))
	iso_conv_layer = iso_conv_layer.replace('NUM_HID2',str(num_hid2))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT1',str(num_out1))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT2',str(num_out2))

	return iso_conv_layer



def first_iso_layer(layer_num,in_bottom,num_hid1,num_hid2,num_out1,num_out2):
	iso_conv_layer = '''
	layer {
	  name: "icLAYER_hid1"
	  type: "Convolution"
	  bottom: "pydata"
	  top: "icLAYER_hid1"
	  convolution_param {
	    num_output: NUM_HID1
	    kernel_size: 3
	    pad: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid1_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid1"
	  top: "icLAYER_hid1"
	}	
	layer {
	  name: "icLAYER_hid2"
	  type: "Convolution"
	  bottom: "icLAYER_hid1"
	  top: "icLAYER_hid2"
	  convolution_param {
	    num_output: NUM_HID2
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_hid2_relu"
	  type: "ReLU"
	  bottom: "icLAYER_hid2"
	  top: "icLAYER_hid2"
	}
	layer {
	  name: "icLAYER_out1"
	  type: "Convolution"
	  bottom: "icLAYER_hid2"
	  top: "icLAYER_out1"
	  convolution_param {
	    num_output: NUM_OUT1
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out1_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out1"
	  top: "icLAYER_out1"
	}
	layer {
	  name: "icLAYER_out2"
	  type: "Convolution"
	  bottom: "icLAYER_out1"
	  top: "icLAYER_out2"
	  convolution_param {
	    num_output: NUM_OUT2
	    kernel_size: 1
	    weight_filler {
	      type: "xavier"
	    }
	  }
	}
	layer {
	  name: "icLAYER_out2_relu"
	  type: "ReLU"
	  bottom: "icLAYER_out2"
	  top: "icLAYER_out2"
	}
	'''

	iso_conv_layer = iso_conv_layer.replace('LAYER',str(layer_num))
	iso_conv_layer = iso_conv_layer.replace('IN_BOTTOM',in_bottom)
	iso_conv_layer = iso_conv_layer.replace('NUM_HID1',str(num_hid1))
	iso_conv_layer = iso_conv_layer.replace('NUM_HID2',str(num_hid2))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT1',str(num_out1))
	iso_conv_layer = iso_conv_layer.replace('NUM_OUT2',str(num_out2))

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
num_hid1 = 128
num_hid2 = 128
num_out1 = 128
num_out2 = 3
layers_dic[layer_num] = first_iso_layer(layer_num,in_bottom,
	num_hid1,num_hid2,num_out1,num_out2)

layer_num = 2
in_bottom = '''	bottom: 'ic1_hid2'
  		bottom: 'ic1_out1' 
  		bottom: 'ic1_out2' '''
layers_dic[layer_num] = iso_layer(layer_num,in_bottom,
	num_hid1,num_hid2,num_out1,num_out2)

for layer_num in range(3,13):
	in_bottom = '''	bottom: 'ic222_out1'
  		bottom: 'ic333_hid2'
  		bottom: 'ic333_out1' '''
  	for l in range(1,layer_num):
  		in_bottom = in_bottom + '''\n bottom: 'ic''' + str(l) +'''_out2' ''' 
  	in_bottom = in_bottom.replace('111',str(layer_num-3))
  	in_bottom = in_bottom.replace('222',str(layer_num-2))
  	in_bottom = in_bottom.replace('333',str(layer_num-1))
	layers_dic[layer_num] = iso_layer(layer_num,in_bottom,
		num_hid1,num_hid2,num_out1,num_out2)

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
'''.replace('BOTTOM',d2n('ic',layer_num,'_out2'))
layer_num += 1
layers_dic[layer_num] = top_layers


proto_str_lst = []
for i in range(layer_num+1):
	proto_str_lst.append(d2s('#### layer', i, '####'))
	proto_str_lst.append(layers_dic[i])

print('\n'.join(proto_str_lst))
list_of_strings_to_txt_file(opjh('Desktop/train_val.prototxt'),proto_str_lst)
	
