from kzpy3.utils2 import *

Network = {}
Network['network_output_sample'] = 4 # >= 0, <= 9
Network['network_steer_gain'] = 3.0
Network['network_motor_gain'] = 1.0
Network['network_motor_offset'] = -2
Network['network_smoothing_parameter'] = 0.33
Network['weight_file_path'] = opjh('pytorch_models','net.infer')

Mse = {}
Mse['HUMAN_SMOOTHING_PARAMETER_1'] = 0.75
