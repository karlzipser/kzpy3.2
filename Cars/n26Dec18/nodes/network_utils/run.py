from kzpy3.utils3 import *
import network_utils.menu_and_net
exec(identify_file_str)



def ready(N):

    for n in CVerbose:
        CVerbose[n] = True
    for n in N['net_hide_colors']:
        CVerbose[n] = False

    cm(10)
    time.sleep(0.0001)
    if N['desktop_mode']:
        N['mode']['human_agent'] = 0
        N['mode']['drive_mode'] = 1
        N['mode']['behavioral_mode'] = 'direct'
        cm(11)
    elif N['mode']['human_agent'] == 0 \
        and N['mode']['drive_mode'] == 1 \
        and N['mode']['behavioral_mode'] in Metadata_tensors.keys():
        cm(12)
        pass
    else:
        cr('human_agent ==',N['mode']['human_agent'],
            'drive_mode ==',N['mode']['drive_mode'],
            'behavioral_mode ==',N['mode']['behavioral_mode'])
        cr('So, not ready for network.')
        return False
    if N['net']['Torch_network'] == None:
        cb('network_node: waiting for network')
        return False
    return True



def step(camera_data,metadata,N):
        cm(16)
        output = N['net']['Torch_network'](camera_data,metadata)
        torch_motor = 100 * output[10+N['network_output_sample']]
        torch_steer = 100 * output[N['network_output_sample']]
        torch_motor = max(0, torch_motor)
        torch_steer = max(0, torch_steer)
        torch_motor = min(99, torch_motor)
        torch_steer = min(99, torch_steer)
        torch_camera = torch_steer
        N['net']['output'] = output
        
        adjusted_camera,adjusted_steer,adjusted_motor = \
            get_adjusted_commands(torch_camera,torch_steer,torch_motor,N)

        camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
        steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
        motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
        frequency_timer.freq(name='network',do_print=True)




def get_adjusted_commands(torch_camera,torch_steer,torch_motor,N):

    sm = N['network_motor_smoothing_parameter']
    ss = N['network_servo_smoothing_parameter']
    if torch_motor >= 49:
        gm = N['network_motor_gain']
    else:
        gm = N['network_reverse_motor_gain']
    gs = N['network_steer_gain']
    gc = N['network_camera_gain']          
    sc = N['network_camera_smoothing_parameter']

    N['out']['current_camera'] = (1.0-sc)*torch_camera + sc*N['out']['current_camera']
    N['out']['current_steer'] = (1.0-ss)*torch_steer + ss*N['out']['current_steer']
    N['out']['current_motor'] = (1.0-sm)*torch_motor + sm*N['out']['current_motor']

    adjusted_motor = int(gm*(N['out']['current_motor']-49) + N['network_motor_offset'] + 49)
    adjusted_steer = int(gs*(N['out']['current_steer']-49) + 49)
    adjusted_camera = int(gc*(N['out']['current_camera']-49) + 49)

    adjusted_motor = bound_value(adjusted_motor,0,99)
    adjusted_steer = bound_value(adjusted_steer,0,99)
    adjusted_camera = bound_value(adjusted_camera,0,99)

    adjusted_motor = min(adjusted_motor,N['max motor'])
    adjusted_motor = max(adjusted_motor,N['min motor'])

    if print_timer.check():
        cg('c:',adjusted_camera,
        '\ts:',adjusted_steer,
        behavioral_mode,'\tm:',
        adjusted_motor,"\t",'network_node__')
        print_timer.reset()

    return adjusted_camera,adjusted_steer,adjusted_motor























#EOF
