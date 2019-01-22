

def read_menu_and_load_network(N):
    
    if not N['timer']['parameter_file_load_timer'].check():
        return

    Topics = menu2.load_Topics(
        opjk("Cars/n26Dec18/nodes"),
        first_load=False,
        customer='Network')

    if type(Topics) == dict:
        for t in Topics.keys():
            if t == 'ABORT':
                if Topics[t] = True:
                    N['ABORT'] = True
                    time.sleep(1)
                    return
        for t in Topics['To Expose']['Network']+\
                 Topics['To Expose']['Weights']+\
                 Topics['To Expose']['Flex']:
            if '!' in t:
                pass
            else:
                N[t] = Topics[t]
    
    if N['LOAD NETWORK'] == False:
        N['net']['loaded_net'] = False
    N['weight_file_path'] = False
    if N['net']['loaded_net'] == False:
        if N['LOAD NETWORK'] == True:
            N['net']['loaded_net'] = True
            ns = N['weight_files'].keys()
            for n in ns:
                if N[n] != False:
                    if type(N[n]) == int:
                        if N[n] != 0:
                            N['weight_file_path'] = \
                                N['weight_files'][n][N[n]]
                            sbpd2s("N['weight_file_path'] = N['weight_files'][n][a[1]]")
                            break
            if N['weight_file_path'] != False:
                cs( "if N['weight_file_path'] != False:" )
                N['net']['Torch_network'] = net_utils.Torch_Network(N)
                cs( "Torch_network = net_utils.Torch_Network(N)" )

    parameter_file_load_timer.reset()



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

        


def step(N):
    for n in CVerbose:
        CVerbose[n] = True
    for n in N['net_hide_colors']:
        CVerbose[n] = False
  

    menu_and_load_network()

    cm(10)
    time.sleep(0.001)

    if Arguments['desktop_mode']:
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
        time.sleep(1)
        cm(13)
        return

    if Torch_network == None:
        cb('network_node: waiting for network')
        time.sleep(2)
        cm(14)
        return    

    if True:#try:
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
        
        adjusted_camera,adjusted_steer,adjusted_motor = get_adjusted_commands(torch_camera,torch_steer,torch_motor,N)

        camera_cmd_pub.publish(std_msgs.msg.Int32(adjusted_camera))
        steer_cmd_pub.publish(std_msgs.msg.Int32(adjusted_steer))
        motor_cmd_pub.publish(std_msgs.msg.Int32(adjusted_motor))
        frequency_timer.freq(name='network',do_print=True)

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)


