from kzpy3.utils3 import *
import network_utils.menu_and_net
import std_msgs.msg
exec(identify_file_str)

CVerbose['magenta'] = False
CCVerbose['magenta'] = False
print_timer = Timer(1/4.)
frequency_timer = Timer(5)

def ready(N):

    for n in CVerbose:
        CVerbose[n] = True
    for n in N['net_hide_colors']:
        CVerbose[n] = False

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

    return True



def step(camera_data,metadata,N):

    output = N['net']['Torch_network']['run_model'](camera_data,metadata)
    #print output
    torch_motor = 100 * output[10+N['network_output_sample']]
    torch_steer = 100 * output[N['network_output_sample']]
    #torch_motor = max(0, torch_motor)
    #torch_steer = max(0, torch_steer)
    #torch_motor = min(99, torch_motor)
    #torch_steer = min(99, torch_steer)

    torch_motor = intr(torch_motor)
    torch_steer = intr(torch_steer)
    #torch_camera = torch_steer
    N['net']['output'] = output

    if print_timer.check():
        if torch_steer > 99 or torch_motor > 99 or torch_steer < 0 or torch_motor < 0:
            cc = cr
            cc(torch_steer,torch_motor)
        else:
            cc = cg
        #cc(torch_steer,torch_motor)
        print_timer.reset()

    #N['pub']['net/camera'].publish(std_msgs.msg.Int32(torch_camera))
    N['pub']['net/steer'].publish(std_msgs.msg.Int32(torch_steer))
    N['pub']['net/motor'].publish(std_msgs.msg.Int32(torch_motor))
    frequency_timer.freq(name='network',do_print=True)































#EOF
