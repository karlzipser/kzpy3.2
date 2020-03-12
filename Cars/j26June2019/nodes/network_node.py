#!/usr/bin/env python
from kzpy3.vis3 import *
import rospy
import network_utils.init
import network_utils.menu_and_net
import network_utils.run
import network_utils.camera
import network_utils.Activity_Module
import default_values
exec(identify_file_str)
import torch
import torch._utils
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2
import kzpy3.VT_net2__1June2019.default_values as VT_net2__1June2019_default_values
#import flex_network_node
N = default_values.P

N['circle_lifetime'] = VT_net2__1June2019_default_values.P['circle_lifetime']
# python kzpy3/Cars/n26Dec18/nodes/network_node.py desktop_mode 1 display 'camera_input' delay_blank 500 delay_prev 500 delay_now 750
# python kzpy3/Cars/n26Dec18/nodes/network_node.py desktop_mode 1 display 'pre_metadata_features_metadata' delay_now 66
for arg,val in [('display',False),('delay_blank',0),('delay_prev',0),('delay_now',1)]:
    if arg not in Arguments:
        Arguments[arg] = val
N['desktop_mode'] = False
if 'desktop_mode' in Arguments:
    if Arguments['desktop_mode']:
        N['desktop_mode'] = True
print_Arguments()
cw(d2s("N['desktop_mode'] ==",N['desktop_mode'],"\t"))



##############################################################################################################
##############################################################################################################
#################################### FLEX NETWORK NODE CODE ##################################################
##############################################################################################################
##############################################################################################################
#############        
if N['use flex']:
    #!/usr/bin/env python
    from kzpy3.vis3 import *
    import kzpy3.Menu_app.menu2 as menu2
    exec(identify_file_str)
    sbpd2s("flex_network_node.py")
    import default_values
    #N = default_values.P
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

    N['flex_weight_file_path'] = most_recent_file_in_folder(opjm('rosbags/Network_Weights/net_flex'))
    #N['flex_weight_file_path'] = most_recent_file_in_folder('/home/karlzipser/Desktop/Network_Weights/net_flex')

    if False:# __name__ == '__main__':
        cg('\nAttempting to run flex_network_node as seperate process, i.e., a rospy node',ra=0)
        rospy.init_node('flex_network_node',anonymous=True,disable_signals=True)
    else:
        cg('/nAttempting to run flex_network_node as thread',ra=0)

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
        try:
            print("Flex_Torch_Network(N):: Start loading...")
            D = {}
            D['save_data'] = torch.load(N['flex_weight_file_path'])
            D['solver'] = SqueezeNet().cuda()
            D['solver'].load_state_dict(D['save_data']['net'])
            D['solver'].eval()
            print("Flex_Torch_Network(N):: Loading complete.")

        except Exception as e:
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



    while True:
        Flex_torch_network = Flex_Torch_Network(N)
        if Flex_torch_network != False:
            #cb(Flex_torch_network,ra=1)
            break
        else:
            cr('failed to load flex network')
            time.sleep(1)

    dimg = zeros((19,18,3))

    for i in range(3):
        cm('waiting to start flex_network_node',i)
        time.sleep(1) # waiting avoids errors because of slow loading of torch

    rate_timer = Timer(1/35.)
    hz = Timer(5)

    def flex_thread(N):
        print_timer = Timer(5);ctr = 0;error_ctr = 0
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



#############        
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################

    






###################################################################
#
rospy.init_node('network_node',anonymous=True,disable_signals=True)
#
###################################################################
#cr(0)
network_utils.init.ros_init(N)
#cr(1)
network_utils.init.metadata_init(N)
#cr(2)

camera_motion_ldr_modulator_timer = Timer(1)
camera_motion_ldr_modulator_notification_Timer = Timer(0.5)
ldr_on_timer = Timer(N['ldr_on_time'])
ldr_off_timer = Timer(N['ldr_off_time'])
#cr(3)
if __name__ == '__main__':

    hz = Timer(10)

    if N['use flex']:
        threading.Thread(target=flex_thread,args=[N]).start()

    while not rospy.is_shutdown() and N['ABORT'] == False:
        #cr(4)
        #if True:
        try:
            network_utils.menu_and_net.read_menu_and_load_network(N)
            #cr(5)
            if network_utils.run.ready(N):
                #cr(6)
                if len(network_utils.camera.Q_list) > 0:
                    #cr(7)
                    Q = network_utils.camera.Q_list[-1]
                    #cr(8)
                    if Q['ready']:
                        #cr(9)             
                        Q['ready'] = False

                        hz.freq(' (main) ')
                        #cm(3)
                        #cr('rectangles_xys' in N)
                        #cr(len(N['rectangles_xys']))
                            
                        if False:
                            if time.time() - N['rectangles_xys_timestamp'] > N['circle_lifetime']:
                                N['rectangles_xys'] = na([])

                        if len(N['rectangles_xys']) > 0:
                            #cr('***')
                            Q['add_rectangles'](N['rectangles_xys'],N['backup parameter'])
                        #cm(4)
                        mci(Q['left']['now']['full'])
                        #cm("mci(Q['left']['now']['full'])")
                        
                        torch_camera_data           = Q['to_torch'](size_='full')
                        #cm(5)
                        torch_small_camera_data    = Q['to_torch'](size_='small')

                        behavioral_mode = N['mode']['behavioral_mode']

                        if behavioral_mode in N['behavioral_metadatas']:
                            torch_metadata = N['behavioral_metadatas'][behavioral_mode]

                        torch_metadata[0,(1+4):(1+4+12),:,:] = torch_small_camera_data

                        ##############################################
                        #
                        if 'ldr_img' in N:

                            if ldr_on_timer.check():
                                ldr_on_timer.time_s = 999
                                ldr_on_timer.reset()
                                ldr_off_timer.time_s = N['ldr_off_time']
                                ldr_off_timer.reset()
                                ldr_on_off = 0.0
                                #cy('ldr_on_off = 0.0')
                            elif ldr_off_timer.check():
                                ldr_off_timer.time_s = 999
                                ldr_off_timer.reset()
                                ldr_on_timer.time_s = N['ldr_on_time']
                                ldr_on_timer.reset()
                                ldr_on_off = 1.0
                                #cg('ldr_on_off = 1.0')

                            current_ldr_gain = N['ldr_gain'] * ldr_on_off

                            ctr = 0
                            
                            for i in [0,2,1]: # center left right [???]
                                m = torch.from_numpy((N['ldr_img'][:,:,i]*1.0)).cuda().float()
                                torch_metadata[0,5+12+ctr,:,:] = m / 255.0 * current_ldr_gain
                                ctr += 1  
                                    
                        else:
                            torch_metadata[0,5+12:5+12+3,:,:] *= 0
                        #
                        ###############################################

                        network_utils.run.step(torch_camera_data,torch_metadata,N)

                        ###############################################
                        #
                        if Arguments['display']:
                            Q2 = network_utils.camera.Quartet('camera from Quartet')
                            
                            if Arguments['display'] == 'camera_input':
                                Q2['from_torch'](N['net']['Torch_network']['solver'].A['camera_input'])
                                size_ = 'full'
                            elif Arguments['display'] == 'pre_metadata_features_metadata':
                                Q2['from_torch'](
                                    N['net']['Torch_network']['solver'].A['pre_metadata_features_metadata'],
                                    offset=128+4+1)
                                size_ = 'small'
                            else:
                                cr("*** Error, could not interpret Arguments['display'] ==",Arguments['display'])
                                assert(False)
                            Q2['display'](
                                delay_blank = Arguments['delay_blank'],
                                delay_prev = Arguments['delay_prev'],
                                delay_now = Arguments['delay_now'],
                                size_=size_)
                        #
                        ###############################################
                                
            else:
                cy("network_utils.run.ready(N) == False")
                time.sleep(2)
        #else:
        except KeyboardInterrupt:
            network_utils.camera.QUIT = True
            cr('\n\n*** KeyboardInterrupt ***\n')
            break
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(
                exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),
                emphasis=False)
        
        
        
    network_utils.camera.QUIT = True

    cg('Exiting network_node.py.')
    raw_enter()

#EOF

    