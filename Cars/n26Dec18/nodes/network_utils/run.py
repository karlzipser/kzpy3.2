from kzpy3.utils3 import *
import network_utils.menu_and_net
import std_msgs.msg
exec(identify_file_str)
#CFile['magenta'] == __file__
CVerbose['magenta'] = False
CCVerbose['magenta'] = False
print_timer = Timer(0)
frequency_timer = Timer(5)

def ready(N):

    for n in CVerbose:
        CVerbose[n] = True
    for n in N['net_hide_colors']:
        CVerbose[n] = False

    ccm(10)
    time.sleep(0.0001)
    if N['desktop_mode']:
        N['mode']['human_agent'] = 0
        N['mode']['drive_mode'] = 1
        N['mode']['behavioral_mode'] = 'direct'
        ccm(11)
    elif N['mode']['human_agent'] == 0 \
        and N['mode']['drive_mode'] == 1 \
        and N['mode']['behavioral_mode'] in N['behavioral_metadatas'].keys():
        ccm(12)
        pass
    else:
        cr('human_agent ==',N['mode']['human_agent'],
            'drive_mode ==',N['mode']['drive_mode'],
            'behavioral_mode ==',N['mode']['behavioral_mode'])
        cr('So, not ready for network.')
        return False
    if N['net']['Torch_network'] == None:
        cb('waiting for network')
        return False
    #ccm('ready')
    return True



def step(camera_data,metadata,N):
    #cg('step')
    ccm(16)
    #raw_enter(d2s("type(N['net']['Torch_network']) =",type(N['net']['Torch_network'])))
    #raw_enter(d2s(N['net']['Torch_network'].keys()))
    output = N['net']['Torch_network']['run_model'](camera_data,metadata)
    #cb("output,type(output) =",output,type(output))
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
    cfun = cg
    if N['flex_motor'] < 47:
        #cm(1)
        cfun = cb
    cfun(adjusted_camera,adjusted_steer,adjusted_motor,N['flex_motor'])
    N['pub']['cmd/camera'].publish(std_msgs.msg.Int32(adjusted_camera))
    N['pub']['cmd/steer'].publish(std_msgs.msg.Int32(adjusted_steer))
    N['pub']['cmd/motor'].publish(std_msgs.msg.Int32(adjusted_motor))
    frequency_timer.freq(name='network',do_print=True)






def get_adjusted_commands(torch_camera,torch_steer,torch_motor,N):

    if N['use flex'] and N['flex_motor'] < 47:
        #cm(0)
        torch_steer = N['flex_steer'] # consider sum
        torch_motor = N['flex_motor']
        sm = N['flex_motor_smoothing_parameter']
        ss = N['flex_servo_smoothing_parameter']
        gm = N['flex_motor_gain']
        gs = N['flex_steer_gain']
        sc = N['network_camera_smoothing_parameter_direct']
        gc = N['network_camera_gain_direct']
    else:
        sm = N['network_motor_smoothing_parameter']

        if torch_motor >= 49:
            if N['mode']['behavioral_mode'] == 'direct':
                gm = N['network_motor_gain_direct']
            else:
                gm = N['network_motor_gain']
        else:
            gm = N['network_reverse_motor_gain']

        if N['mode']['behavioral_mode'] == 'direct':
            ss = N['network_servo_smoothing_parameter_direct']
            gs = N['network_steer_gain_direct']
            gc = N['network_camera_gain_direct']          
            sc = N['network_camera_smoothing_parameter_direct']
        else:
            ss = N['network_servo_smoothing_parameter']
            gs = N['network_steer_gain']
            gc = N['network_camera_gain']          
            sc = N['network_camera_smoothing_parameter']


    N['current']['camera'] = (1.0-sc)*torch_camera + sc*N['current']['camera']
    N['current']['steer'] = (1.0-ss)*torch_steer + ss*N['current']['steer']
    N['current']['motor'] = (1.0-sm)*torch_motor + sm*N['current']['motor']

    adjusted_motor = int(gm*(N['current']['motor']-49) + N['network_motor_offset'] + 49)
    adjusted_steer = int(gs*(N['current']['steer']-49) + 49)
    adjusted_camera = int(gc*(N['current']['camera']-49) + 49)

    adjusted_motor = bound_value(adjusted_motor,0,99)
    adjusted_steer = bound_value(adjusted_steer,0,99)
    adjusted_camera = bound_value(adjusted_camera,0,99)

    adjusted_motor = min(adjusted_motor,N['max motor'])
    adjusted_motor = max(adjusted_motor,N['min motor'])

    #print(format_row([('s',adjusted_steer),('c',adjusted_camera),('m',adjusted_motor)]))
    """
    if print_timer.check():
        cg('c:',adjusted_camera,
        '\ts:',adjusted_steer,
        N['mode']['behavioral_mode'],'\tm:',
        adjusted_motor,"\t",file)
        print_timer.reset()
    """
    return adjusted_camera,adjusted_steer,adjusted_motor























#EOF
