from kzpy3.utils import *



def write_cccp_later(CONV,BOTTOM,NUM_OUTPUT,KERNEL_SIZE,STRIDE):
	cccp_layer_str = """

###############################################################
#
layer {
  name: "CONV"
  type: "Convolution"
  bottom: "BOTTOM"
  top: "CONV"
  convolution_param {
    num_output: NUM_OUTPUT
    kernel_size: KERNEL_SIZE
    pad: KERNEL_SIZE
    stride: STRIDE
    weight_filler {
      type: "xavier"
    }
  }
}
layer {
  name: "RELU1_CONV"
  type: "ReLU"
  bottom: "CONV"
  top: "CONV"
}
layer {
  name: "CCCP1_CONV"
  type: "Convolution"
  bottom: "CONV"
  top: "CCCP1_CONV"
  convolution_param {
    num_output: NUM_OUTPUT
    kernel_size: 1
    stride: 1
    weight_filler {
      type: "xavier"
    }
  }
}
layer {
  name: "RELU2_CONV"
  type: "ReLU"
  bottom: "CCCP1_CONV"
  top: "CCCP1_CONV"
}
layer {
  name: "CCCP2_CONV"
  type: "Convolution"
  bottom: "CCCP1_CONV"
  top: "CCCP2_CONV"
  convolution_param {
    num_output: NUM_OUTPUT
    kernel_size: 1
    stride: 1
    weight_filler {
      type: "xavier"
    }
  }
}
layer {
  name: "RELU3_CONV"
  type: "ReLU"
  bottom: "CCCP2_CONV"
  top: "CCCP2_CONV"
}
layer {
  name: "POOL_CONV"
  type: "Pooling"
  bottom: "CCCP2_CONV"
  top: "POOL_CONV"
  pooling_param {
    pool: MAX
    kernel_size: 3
    stride: 2
  }
}
#
###############################################################


	"""

	new_cccp = cccp_layer_str.replace('CONV',CONV)
	new_cccp = new_cccp.replace('BOTTOM',BOTTOM)
	new_cccp = new_cccp.replace('NUM_OUTPUT',str(NUM_OUTPUT))
	new_cccp = new_cccp.replace('KERNEL_SIZE',str(KERNEL_SIZE))
	new_cccp = new_cccp.replace('STRIDE',str(STRIDE))

	return new_cccp


