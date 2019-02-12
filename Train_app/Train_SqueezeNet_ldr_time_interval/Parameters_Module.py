from Paths_Module import *
exec(identify_file_str)

P = {}

P['start time'] = time_str()
P['start time numeric'] = time.time()


P['GPU'] = 0 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['BATCH_SIZE'] = 64
P['REQUIRE_ONE'] = []
P['NETWORK_OUTPUT_FOLDER'] = opjD('net_flex')#opjD('net_16Aug2018')#opjD('net_16Aug2018')# #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P['SAVE_FILE_NAME'] = 'net'
P['save_net_timer'] = Timer(60*15)
P['print_timer'] = Timer(5)
P['print_timer2'] = Timer(30)
P['frequency_timer'] = Timer(10.0)
P['TRAIN_TIME'] = 60*5.0
P['VAL_TIME'] = 60*1.0
P['RESUME'] = True
if P['RESUME']:
    P['INITIAL_WEIGHTS_FOLDER'] = opj(P['NETWORK_OUTPUT_FOLDER'],'weights')
    P['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(P['INITIAL_WEIGHTS_FOLDER'],['net'],[])	
P['reload_image_file_timer'] = Timer(5*60)
P['loss_timer'] = Timer(60*10/10)
P['LOSS_LIST_N'] = 30









#EOF