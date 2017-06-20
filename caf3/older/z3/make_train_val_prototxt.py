from kzpy3.utils import *

solver1_all_layers = ""

solver1_layers = """
############################################
#
layer {
	name: "steer_motor_target_data__%s"
	type: "DummyData"
	top: "steer_motor_target_data__%s"
	dummy_data_param {
		shape {
			dim: 1
			dim: 20
		}
	}
}



layer {
	name: "metadata__%s"
	type: "DummyData"
	top: "metadata__%s"
	dummy_data_param {
		shape {
			dim: 1
			dim: 6
			dim: 14
			dim: 26
		}
	}
}


layer {
	name: "ZED_data_pool2__%s"
	type: "DummyData"
	top: "ZED_data_pool2__%s"
	dummy_data_param {
		shape {
			dim: 1
			dim: 4
			dim: 94
			dim: 168
		}
	}
}

layer {
	name: "conv1__%s"
	type: "Convolution"
	bottom: "ZED_data_pool2__%s"
	top: "conv1__%s"
	convolution_param {
		num_output: 96
		group: 1
		kernel_size: 11
		stride: 3
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv1_relu__%s"
	type: "ReLU"
	bottom: "conv1__%s"
	top: "conv1__%s"
}
	
layer {
	name: "conv1_pool__%s"
	type: "Pooling"
	bottom: "conv1__%s"
	top: "conv1_pool__%s"
	pooling_param {
		pool: MAX
		kernel_size: 3
		stride: 2
		pad: 0
	}
}
	
layer {
  name: "conv1_metadata_concat__%s"
  type: "Concat"
  bottom: "conv1_pool__%s"
  bottom: "metadata__%s"
  top: "conv1_metadata_concat__%s"
  concat_param {
    axis: 1
  }
}

layer {
	name: "conv2__%s"
	type: "Convolution"
	bottom: "conv1_metadata_concat__%s"
	top: "conv2__%s"
	convolution_param {
		num_output: 256
		group: 2
		kernel_size: 3
		stride: 2
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv2_relu__%s"
	type: "ReLU"
	bottom: "conv2__%s"
	top: "conv2__%s"
}
	

"""


for n in range(8):
	nums = []
	for i in range(25):
		nums.append(str(n))
	nums = tuple(nums)
	solver1_all_layers  += solver1_layers % nums


solver2_all_layers = ""
solver2_layers = """
############################################
#
layer {
  name: "conv2_time_concat__%s"
  type: "Concat"
  bottom: "conv2__%s"
  bottom: "conv2__%s"
  top: "conv2_time_concat__%s"
  concat_param {
    axis: 1
  }
}

layer {
	name: "conv2_2__%s"
	type: "Convolution"
	bottom: "conv2_time_concat__%s"
	top: "conv2_2__%s"
	convolution_param {
		num_output: 256
		group: 1
		kernel_size: 1
		stride: 1
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv2_2_relu__%s"
	type: "ReLU"
	bottom: "conv2_2__%s"
	top: "conv2_2__%s"
}

layer {
	name: "conv3_2__%s"
	type: "Convolution"
	bottom: "conv2_2__%s"
	top: "conv3_2__%s"
	convolution_param {
		num_output: 384
		group: 2
		kernel_size: 3
		stride: 2
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv3_2_relu__%s"
	type: "ReLU"
	bottom: "conv3_2__%s"
	top: "conv3_2__%s"
}
"""


for n in range(4):
	nums = []
	ns = [n, 2*n, 2*n+1, n, n, n, n, n, n, n, n, n, n, n, n, n]
	for i in range(len(ns)):
		nums.append(str(ns[i]))
	nums = tuple(nums)
	solver2_all_layers += solver2_layers % nums


solver3_all_layers = ""
solver3_layers = """
############################################
#
layer {
  name: "conv3_2_time_concat__%s"
  type: "Concat"
  bottom: "conv3_2__%s"
  bottom: "conv3_2__%s"
  top: "conv3_2_time_concat__%s"
  concat_param {
    axis: 1
  }
}

layer {
	name: "conv3_2_2__%s"
	type: "Convolution"
	bottom: "conv3_2_time_concat__%s"
	top: "conv3_2_2__%s"
	convolution_param {
		num_output: 384
		group: 1
		kernel_size: 1
		stride: 1
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv3_2_2_relu__%s"
	type: "ReLU"
	bottom: "conv3_2_2__%s"
	top: "conv3_2_2__%s"
}

layer {
	name: "conv4_2__%s"
	type: "Convolution"
	bottom: "conv3_2_2__%s"
	top: "conv4_2__%s"
	convolution_param {
		num_output: 384
		group: 2
		kernel_size: 3
		stride: 1
		pad: 1
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv4_2_relu__%s"
	type: "ReLU"
	bottom: "conv4_2__%s"
	top: "conv4_2__%s"
}

"""

for n in range(2):
	nums = []
	ns = [n, 2*n, 2*n+1, n, n, n, n, n, n, n, n, n, n, n, n, n]
	for i in range(len(ns)):
		nums.append(str(ns[i]))
	nums = tuple(nums)
	solver3_all_layers += solver3_layers % nums


solver4_all_layers = ""
solver4_layers = """
############################################
#
layer {
  name: "conv4_2_time_concat__%s"
  type: "Concat"
  bottom: "conv4_2__%s"
  bottom: "conv4_2__%s"
  top: "conv4_2_time_concat__%s"
  concat_param {
    axis: 1
  }
}

layer {
	name: "conv4_2_2__%s"
	type: "Convolution"
	bottom: "conv4_2_time_concat__%s"
	top: "conv4_2_2__%s"
	convolution_param {
		num_output: 384
		group: 1
		kernel_size: 1
		stride: 1
		pad: 0
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv4_2_2_relu__%s"
	type: "ReLU"
	bottom: "conv4_2_2__%s"
	top: "conv4_2_2__%s"
}

layer {
	name: "conv5_2__%s"
	type: "Convolution"
	bottom: "conv4_2_2__%s"
	top: "conv5_2__%s"
	convolution_param {
		num_output: 384
		group: 2
		kernel_size: 3
		stride: 1
		pad: 1
		weight_filler {
			type: "gaussian" 
			std: 0.1
		}
	}
}
	
layer {
	name: "conv5_2_relu__%s"
	type: "ReLU"
	bottom: "conv5_2__%s"
	top: "conv5_2__%s"
}

"""

for n in range(1):
	nums = []
	ns = [n, 2*n, 2*n+1, n, n, n, n, n, n, n, n, n, n, n, n, n]
	for i in range(len(ns)):
		nums.append(str(ns[i]))
	nums = tuple(nums)
	solver4_all_layers += solver4_layers % nums


ip_layers = """
############################################
#
layer {
	name: "ip1_conv2_2"
	type: "InnerProduct"
	bottom: "conv2__7"
	top: "ip1_conv2_2"
	inner_product_param {
		num_output: 512
		weight_filler {
			type: "xavier" 
		}
	}
}
layer {
	name: "ip1_conv2_2_relu"
	type: "ReLU"
	bottom: "ip1_conv2_2"
	top: "ip1_conv2_2"
}

layer {
	name: "ip1_conv3_2"
	type: "InnerProduct"
	bottom: "conv3_2__3"
	top: "ip1_conv3_2"
	inner_product_param {
		num_output: 512
		weight_filler {
			type: "xavier" 
		}
	}
}
layer {
	name: "ip1_conv3_2_relu"
	type: "ReLU"
	bottom: "ip1_conv3_2"
	top: "ip1_conv3_2"
}

layer {
	name: "ip1_conv4_2"
	type: "InnerProduct"
	bottom: "conv4_2__1"
	top: "ip1_conv4_2"
	inner_product_param {
		num_output: 512
		weight_filler {
			type: "xavier" 
		}
	}
}
layer {
	name: "ip1_conv4_2_relu"
	type: "ReLU"
	bottom: "ip1_conv4_2"
	top: "ip1_conv4_2"
}


layer {
	name: "ip1_conv5_2"
	type: "InnerProduct"
	bottom: "conv5_2__0"
	top: "ip1_conv5_2"
	inner_product_param {
		num_output: 512
		weight_filler {
			type: "xavier" 
		}
	}
}

layer {
	name: "ip1_conv5_2_relu"
	type: "ReLU"
	bottom: "ip1_conv5_2"
	top: "ip1_conv5_2"
}


layer {
  name: "ip1_concat"
  type: "Concat"
  bottom: "ip1_conv2_2"
  bottom: "ip1_conv3_2"
  bottom: "ip1_conv4_2"
  bottom: "ip1_conv5_2"
  top: "ip1_concat"
  concat_param {
    axis: 1
  }
}

layer {
	name: "ip1_2"
	type: "InnerProduct"
	bottom: "ip1_concat"
	top: "ip1_2"
	inner_product_param {
		num_output: 96
		weight_filler {
			type: "xavier" 
		}
	}
}

layer {
	name: "ip2"
	type: "InnerProduct"
	bottom: "ip1_2"
	top: "ip2"
	inner_product_param {
		num_output: 20
		weight_filler {
			type: "xavier" 
		}
	}
}

"""

prototxt = solver1_all_layers + solver2_all_layers + solver3_all_layers + solver4_all_layers + ip_layers

list_of_strings_to_txt_file(opjh('kzpy3','caf3','z3','train_val_unified.prototxt'),[prototxt])
