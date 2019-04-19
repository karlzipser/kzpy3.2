#!/usr/bin/env python
from kzpy3.vis3 import *
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)
sbpd2s("flex_network_node.py")
import default_values
N = default_values.P
if not N['use flex']:
    cb("Not using flex_network_node")
    while not rospy.is_shutdown():
        time.sleep(10)
import rospy
import kzpy3.Data_app.collect_flex_data2 as fx
import roslib
import std_msgs.msg
import torch
import torch.nn as nn
from torch.autograd import Variable
exec(identify_file_str)

N['flex_weight_file_path'] = most_recent_file_in_folder(opjm('rosbags/net_flex'))
#N['flex_weight_file_path'] = most_recent_file_in_folder('/home/karlzipser/Desktop/Network_Weights/net_flex')

if __name__ == '__main__':
    cg('\nAttempting to run flex_network_node as seperate process, i.e., a rospy node',ra=0)
    rospy.init_node('flex_network_node',anonymous=True,disable_signals=True)
else:
    cg('/nAttempting to run flex_network_node as thread',ra=1)

flex_names = default_values.flex_names

F = {}
for f in flex_names:
    s = """
F['FLEX'] = []
def FLEX__callback(msg):
    adjusted_data = msg.data * N['FLEX/gain']
    advance(F['FLEX'],adjusted_data,18)
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
    """
    exec_str = s.replace('FLEX',f)
    exec(exec_str)

flex_steer_cmd_pub = rospy.Publisher('flex/steer', std_msgs.msg.Float32, queue_size=5)
flex_motor_cmd_pub = rospy.Publisher('flex/motor', std_msgs.msg.Float32, queue_size=5)



from kzpy3.Train_app.nets.SqueezeNet_flex import SqueezeNet


def Flex_Torch_Network(N):
    global ready_to_run
    if True:#try:
        D = {}
        D['save_data'] = torch.load(N['flex_weight_file_path'])
        D['solver'] = SqueezeNet().cuda()
        D['solver'].load_state_dict(D['save_data']['net'])
        D['solver'].eval()
        print("Flex_Torch_Network(N):: Loading complete.")

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        return False

    def _run_model(input,N):
        D['output'] = D['solver'](input)
        torch_motor = 100 * D['output'][0][18+N['flex_network_output_sample']].data[0].cpu().numpy()
        torch_steer = 100 * D['output'][0][N['flex_network_output_sample']].data[0].cpu().numpy()
        return torch_motor, torch_steer

    def _format_flex_data(img):
        flex_data = torch.FloatTensor().cuda()
        list_camera_input = []
        list_camera_input.append(torch.from_numpy(img))
        camera_data = torch.cat(list_camera_input, 2)
        camera_data = camera_data.cuda().float()/4000.0
        camera_data = torch.transpose(camera_data, 0, 2)
        camera_data = torch.transpose(camera_data, 1, 2)
        flex_data = torch.cat((torch.unsqueeze(camera_data, 0), flex_data), 0)
        flex_data = Variable(flex_data)
        return flex_data

    D['run_model'] = _run_model
    D['format_flex_data'] = _format_flex_data

    return D


parameter_file_load_timer = Timer(2)

print_timer = Timer(5);ctr = 0;error_ctr = 0

while True:
    Flex_torch_network = Flex_Torch_Network(N)
    if Flex_torch_network != False:
        #cb(Flex_torch_network,ra=1)
        break
    else:
        cr('failed to load flex network')
        time.sleep(1)

dimg = zeros((19,18,3))

for i in range(10):
    cm('waiting to start flex_network_node',i)
    time.sleep(1) # waiting avoids errors because of slow loading of torch

rate_timer = Timer(1/35.)
hz = Timer(5)

while not rospy.is_shutdown() and not N['ABORT']:

    if rate_timer.check():
        rate_timer.reset()
        try:
            hz.freq('flex')

            if parameter_file_load_timer.check():

                Topics = menu2.load_Topics(
                    N['project_path'],
                    first_load=False,
                    customer='Flex')
                
                if type(Topics) == dict:
                    for t in Topics['To Expose']['Flex']:
                        if '!' in t:
                            pass
                        else:
                            N[t] = Topics[t]

                parameter_file_load_timer.reset()

            print_timer.message(d2s("ctr,error =",ctr,',',error_ctr));ctr+=1
            time.sleep(0.01)

            img3 = na(fx.make_flex_image(F))

            flex_data = Flex_torch_network['format_flex_data'](img3)
            flex_torch_motor, flex_torch_steer = Flex_torch_network['run_model'](flex_data, N)

            flex_steer_cmd_pub.publish(std_msgs.msg.Float32(flex_torch_steer))
            flex_motor_cmd_pub.publish(std_msgs.msg.Float32(flex_torch_motor))

            if N['flex_graphics']:
                dimg[fx.num_backward_timesteps,:,:]=2000
                dimg[fx.num_backward_timesteps,0,:]=-2000
                dimg[:fx.num_backward_timesteps,:,:] = img3
                mci(z55(dimg),
                    scale=12.0,
                    delay=1,
                    title='flex net input')
        except Exception as e:
            error_ctr += 1
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    else:
        time.sleep(0.001)

        
#EOF

    
