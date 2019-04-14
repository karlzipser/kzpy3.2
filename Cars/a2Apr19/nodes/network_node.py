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
N = default_values.P

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

###################################################################
#
rospy.init_node('network_node',anonymous=True,disable_signals=True)
#
###################################################################

network_utils.init.ros_init(N)

network_utils.init.metadata_init(N)



if __name__ == '__main__':

    hz = Timer(10)

    while not rospy.is_shutdown() and N['ABORT'] == False:

        if True:#try:
            network_utils.menu_and_net.read_menu_and_load_network(N)

            if network_utils.run.ready(N):

                if len(network_utils.camera.Q_list) > 0:

                    Q = network_utils.camera.Q_list[-1]
                    if Q['ready']:
                        
                        #Q['display'](size_='full',delay_now=1)
                        
                        Q['ready'] = False

                        hz.freq(' (main) ')

                        torch_camera_data           = Q['to_torch'](size_='full')

                        torch_small_camera_data    = Q['to_torch'](size_='small')

                        behavioral_mode = N['mode']['behavioral_mode']

                        if behavioral_mode in N['behavioral_metadatas']:
                            torch_metadata = N['behavioral_metadatas'][behavioral_mode]

                        torch_metadata[0,(1+4):(1+4+12),:,:] = torch_small_camera_data

                        if 'ldr_img' in N:

                            mci(N['ldr_img'],color_mode=cv2.COLOR_RGB2BGR,delay=33,title='network_node.py /ldr',scale=8)
                            ctr = 0
                            if True:
                                for i in [0,2,1]: # center left right
                                    #mi(N['ldr_img'][:,:,i],i)
                                    torch_metadata[0,5+12+ctr,:,:] = torch.from_numpy((N['ldr_img'][:,:,i]*1.0)).cuda().float()/255.0
                                    ctr += 1
                            #spause()
                            #mci()
                        network_utils.run.step(torch_camera_data,torch_metadata,N)

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
                                
            else:
                cy("network_utils.run.ready(N) == False")
                time.sleep(2)
        """
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
        """
        
        
    network_utils.camera.QUIT = True
    cm(103)
    cg('Exiting network_node.py.')


#EOF

    