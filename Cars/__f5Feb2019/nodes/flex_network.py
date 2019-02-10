#!/usr/bin/env python
from kzpy3.vis3 import *
import kzpy3.Menu_app.menu2 as menu2
exec(identify_file_str)
sbpd2s("flex_network_node.py")
import default_values
N = default_values.P
QUIT = False
if not N['use flex']:
    cb("Not using flex_network_node")
    while not rospy.is_shutdown():
        time.sleep(10)

import rospy
import kzpy3.Data_app.collect_flex_data2 as fx
import roslib
import std_msgs.msg
import rospy

if False: #put this in
    sm = N['flex_motor_smoothing_parameter']
    ss = N['flex_servo_smoothing_parameter']
    gm = N['flex_motor_gain']
    gs = N['flex_steer_gain']
    sc = N['network_camera_smoothing_parameter_direct']
    gc = N['network_camera_gain_direct']

################################################################
#
if __name__ == '__main__':
    rospy.init_node('flex_network_node',anonymous=True,disable_signals=True)
#
################################################################

button_number = 0

def button_number_callback(msg):
    global button_number
    button_number = msg.data

rospy.Subscriber('/bair_car/button_number', std_msgs.msg.Int32, callback=button_number_callback)

flex_names = default_values.flex_names

F = {}
for f in flex_names:
    s = """
F['FLEX'] = []
#F['FLEX_ts'] = []
def FLEX__callback(msg):
    #F['FLEX'].append(msg.data)
    #if len(F['FLEX']) > 18:
    #    F['FLEX'] = F['FLEX'][-18:]
    adjusted_data = msg.data * N['FLEX/gain']
    advance(F['FLEX'],adjusted_data,18)
    #advance(F['FLEX_ts'],time.time(),18)
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
    """
    exec_str = s.replace('FLEX',f)
    exec(exec_str)

flex_steer_cmd_pub = rospy.Publisher('cmd/flex_steer', std_msgs.msg.Int32, queue_size=5)
flex_motor_cmd_pub = rospy.Publisher('cmd/flex_motor', std_msgs.msg.Int32, queue_size=5)

import torch
import torch.nn as nn
from torch.autograd import Variable
exec(identify_file_str)
import rospy
from kzpy3.Train_app.nets.SqueezeNet_flex import SqueezeNet



def Flex_Torch_Network(N):
    global ready_to_run
    if True: #try:
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
    def _run_model(input,N):
        D['output'] = D['solver'](input)
        if N['flex_graphics']:
            st = []
            for i in range(18):
                st.append(D['output'][0][i].data[0].cpu().numpy())
            st  = 99*na(st)
            st = st.astype(int)
            mt = []
            for i in range(18):
                mt.append(D['output'][0][i+18].data[0].cpu().numpy())
            mt  = 99*na(mt)
            mt = mt.astype(int) 
            figure('output')
            clf()

            plot(99*np.squeeze(D['output'][0][:].data[:].cpu().numpy()),'k.')
            plot(range(0,18),st,'r-')
            plot(range(18,36),mt,'b-')
            plot([0,36],[49,49],'g')
            ylim(0,99)
            spause()
        torch_motor = 100 * D['output'][0][18+N['flex_network_output_sample']].data[0].cpu().numpy()
        torch_steer = 100 * D['output'][0][N['flex_network_output_sample']].data[0].cpu().numpy()
        torch_motor = max(0, torch_motor[0])
        torch_steer = max(0, torch_steer[0])
        torch_motor = min(99, torch_motor)
        torch_steer = min(99, torch_steer)

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




parameter_file_load_timer = Timer(1)

print_timer = Timer(5);ctr = 0;error_ctr = 0
hz = Timer(5)

Flex_torch_network = Flex_Torch_Network(N)

dimg = zeros((19,18,3))

#time.sleep(10) # waiting avoids errors because of slow loading of torch

def flex_thread():
    global ctr,error_ctr
    while not rospy.is_shutdown() and QUIT == False:

        try:

            if button_number == 4:

                time.sleep(0.5)

                if parameter_file_load_timer.check():

                    Topics = menu2.load_Topics(
                        pname(__file__),
                        first_load=False,
                        customer='Flex')
                    
                    if type(Topics) == dict:
                        for t in Topics['To Expose']['Flex']+Topics['To Expose']['Flex']:
                            if '!' in t:
                                pass
                            else:
                                N[t] = Topics[t]

                    parameter_file_load_timer.reset()

                continue


            print_timer.message(d2s("ctr,error =",ctr,',',error_ctr));ctr+=1
            time.sleep(0.01)

            try:
                img3 = na(fx.make_flex_image(F))
            except:
                #cr('img3 = na(fx.make_flex_image(F))')
                time.sleep(0.1)
                continue

            flex_data = Flex_torch_network['format_flex_data'](img3)
            flex_torch_motor, flex_torch_steer = Flex_torch_network['run_model'](flex_data, N)
            hz.freq('flex network')

            flex_torch_motor = min(flex_torch_motor,N['flex max motor'])
            flex_torch_motor = max(flex_torch_motor,N['flex min motor'])

            ################################################################
            ################################################################
            ### publish
            flex_steer_cmd_pub.publish(std_msgs.msg.Int32(flex_torch_steer))
            flex_motor_cmd_pub.publish(std_msgs.msg.Int32(flex_torch_motor))
            ###
            ################################################################
            ################################################################

            if False:
                print(format_row([('S',flex_torch_steer),('M',flex_torch_motor)]))

            if N['flex_graphics']:
                dimg[fx.num_backward_timesteps,:,:]=2000
                dimg[fx.num_backward_timesteps,0,:]=-2000
                dimg[:fx.num_backward_timesteps,:,:] = img3
                mi(z2o(dimg),'img');spause()

        except Exception as e:
            error_ctr += 1
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

        
if __name__ == '__main__':
    flex_thread()
#EOF

    