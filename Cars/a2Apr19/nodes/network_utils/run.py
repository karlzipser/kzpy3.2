from kzpy3.utils3 import *
import network_utils.menu_and_net
import std_msgs.msg
exec(identify_file_str)

print_timer = Timer(1/4.)
frequency_timer = Timer(5)

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
        and N['mode']['behavioral_mode'] in N['behavioral_metadatas'].keys():
        cm(12)
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
    #cm('ready')
    return True



def step(camera_data,metadata,N):

    output = N['net']['Torch_network']['run_model'](camera_data,metadata)

    torch_motor = 100. * output[10+N['network_output_sample']]
    torch_steer = 100. * output[N['network_output_sample']]

    
    N['net']['output'] = output

    if print_timer.check():
        if torch_steer > 99 or torch_steer < 0 or torch_motor > 99 or torch_motor < 0:
            cfun = cr
        else:
            cfun = cg
        cfun(int(torch_steer),int(torch_motor),N['mode']['behavioral_mode'])
        print_timer.reset()

    N['pub']['net/steer'].publish(std_msgs.msg.Float32(torch_steer))
    N['pub']['net/motor'].publish(std_msgs.msg.Float32(torch_motor))


    N['pub']['net/encoder0'].publish(data=1000*output[-30:-20])
    N['pub']['net/encoder1'].publish(data=1000*output[-20:-10])
    N['pub']['net/encoder2'].publish(data=1000*output[-10:])

    N['pub']['net/header0'].publish(data=1000*output[-60:-50])
    N['pub']['net/header1'].publish(data=1000*output[-50:-40])
    N['pub']['net/header2'].publish(data=1000*output[-40:-30])

    N['pub']['net/motor0'].publish(data=100*output[-90:-80])
    N['pub']['net/motor1'].publish(data=100*output[-80:-70])
    N['pub']['net/motor2'].publish(data=100*output[-70:-60])

    if True:
        cr((output[-60:-50]*1000).astype(int)/1000.0)
        cb((output[-50:-40]*1000).astype(int)/1000.0)
        cg((output[-40:-30]*1000).astype(int)/1000.0)


    frequency_timer.freq(name='network',do_print=True)



#EOF
