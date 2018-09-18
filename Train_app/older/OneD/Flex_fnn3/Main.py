from kzpy3.vis3 import *

#
############################
#
import torch
import torch.nn as nn
from torch.autograd import Variable
#
############################
#

from default_values import *
import prepare_data # import *#from kzpy3.Train_app.Train_fnn1.prepare_data import *
P = prepare_data.P
exec(identify_file_str)

for k in P:
    k_short_safe = k.split('/')[-1].replace(' ','_').replace(',','__').replace('.','').replace('!','')
    ex_str = d2n(k_short_safe,' = ',"P['",k,"']")
    print ex_str
    exec(ex_str)


if P['autostart menu thread']:
    ############# start menu thread ############
    #
    import kzpy3.Menu_app.menu
    __default_values_module_name__ = "kzpy3.Train_app.OneD.Flex_fnn2.default_values"
    __topics_dic_name__ = "P"
    exec(kzpy3.Menu_app.menu.__MENU_THREAD_EXEC_STR__.replace(
        '__default_values_module_name__',__default_values_module_name__
        ).replace('__topics_dic_name__',__topics_dic_name__))
    #
    ############################################


if P['LIVE']:
    CS('Setting up ROS')
    import roslib
    import std_msgs.msg
    import geometry_msgs.msg
    import rospy
    Mean_std = {
        'acc_x': [-0.2, 1.1],
        'acc_y': [9.8, 1.1],
        'acc_z': [0.7, 1.2],
        'encoder': [1.7, 1.3],
        'gyro_heading_x': [213.7, 519.1],
        'gyro_heading_y': [-111.2, 177.1],
        'gyro_heading_z': [150.3, 202.4],
        'gyro_x': [-0.1, 10.7],
        'gyro_y': [0.1, 9.8],
        'gyro_z': [-0.1, 8.4],
        'xfc0': [-3.4, 157.1],
        'xfl0': [10.8, 45.5],
        'xfl1': [-41.1, 831.0],
        'xfr0': [23.0, 50.4],
        'xfr1': [-0.6, 24.5],
    }

    flex_names = []
    for fb in ['f','b']:
        for lr in ['l','r','c']:
            for i in [0,1]:
                flex_names.append(d2n('x',fb,lr,i))
    flex_names.append('xan0')
    R = {}
    GC = 0
    for f in flex_names:
        R[f] = {}
        R[f]['ts'] = []
        R[f]['vals'] = []
        s = """
def FLEX__callback(msg):
\tglobal GC
\tGC += 1
\t#R['FLEX']['ts'].append(time.time())
\t#R['FLEX']['vals'].append(msg.data)
\tadvance(R['FLEX']['ts'],time.time(),min_len=P['net/num input timesteps.'])
\tadvance(R['FLEX']['vals'],msg.data,min_len=P['net/num input timesteps.'])
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
        """
        exec_str = s.replace('FLEX',f)
        print exec_str
        exec(exec_str)

    rospy.init_node('listener',anonymous=True)


 
 


############################
#
spd2s(username,P['sys/GPU.'])
if P['sys/use cuda']:
    torch.cuda.set_device(P['sys/GPU.'])
    torch.cuda.device(P['sys/GPU.'])

class Net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
#
############################





"""
############################
#
class Net(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.lr = 0.1
        self.momentum = 0.00000001
        i0=5
        i1=20
        i2=20
        i3=20
        self.conv1 = nn.Conv1d(in_channels=i0, out_channels=i1, kernel_size=6, stride=2, groups=1)
        self.conv2 = nn.Conv1d(in_channels=i1, out_channels=i2, kernel_size=6, stride=2, groups=1)
        self.conv3 = nn.Conv1d(in_channels=i2, out_channels=i3, kernel_size=6, stride=2, groups=1)
        self.ip1 = nn.Linear(in_features=80, out_features=20)
        self.ip2 = nn.Linear(in_features=20, out_features=20)
        #nn.init.normal(self.conv1.weight, std=1.0)
        #nn.init.normal(self.conv2.weight, std=1.0)
        #nn.init.normal(self.conv3.weight, std=1.0)
        #nn.init.normal(self.ip1.weight, std=1.0)
        #nn.init.normal(self.ip2.weight, std=1.0)
        #nn.init.xavier_normal(self.ip1.weight)
        #nn.init.xavier_normal(self.ip2.weight)
        self.C={}
    
    def forward(self, x):
        self.C['input'] = x
        self.C['conv1'] = self.conv1(self.C['input'])
        self.C['conv1/relu'] = F.relu(self.C['conv1'])
        self.C['conv2'] = self.conv2(self.C['conv1/relu'])
        self.C['conv2/relu'] = F.relu(self.C['conv2'])
        self.C['conv3'] = self.conv2(self.C['conv2/relu'])
        self.C['conv3/relu'] = F.relu(self.C['conv3'])
        #print self.C['conv3/relu'].size()
        #self.C['conv3/flat'] = self.C['conv3/relu'].view(self.C['conv3/relu'].size()[0],-1)
        self.C['conv3/flat'] = self.C['conv3/relu'].view(-1,80)
        self.C['ip1'] = self.ip1(self.C['conv3/flat'])
        #self.C['ip1/relu'] = F.relu(self.C['ip1'])
        #self.C['ip2'] = self.ip1(self.C['ip1/relu'])
        self.C['output'] = self.C['ip1']
        return self.C['output']
#
############################
"""



















reminder_timer = Timer(10)
reminder_timer.trigger()


temp_timer = Timer(30)
while False:#not temp_timer.check():
    print R['xfc0']['vals'][-1]
#
############################
#
P['net/net!'] = Net(input_size, hidden_size, output_size)#.cuda()
if P['sys/use cuda']:
    P['net/net!'] = P['net/net!'].cuda()
#
############################
#

_random_weights = True
spd2s(P['net/net!'])
if P['cmd/resume from saved state.']:
    try:
        spd2s("P['cmd/resume from saved state.'] = True")
        latest_weights = most_recent_file_in_folder(opj(P['path/processed data location.'],'weights'))
        spd2s("latest_weights = ",latest_weights)
#
############################
#
        saved_net = torch.load(latest_weights)

        P['net/net!'].load_state_dict(saved_net)
        spd2s(P['net/net!'])
#
############################
#
        CS_(d2s('resuming with weight file',latest_weights),section=fname(__file__))
        _random_weights = False
    except:
        CS_(d2s('failed to load weights!'),section=fname(__file__),exception=True)
        exec(EXCEPT_STR)
if P['LIVE']:
    assert _random_weights == False
    assert batch_size == 1

if _random_weights:
    CS_('training with random weights',fname(__file__))
#
############################
#
inputs = torch.FloatTensor(batch_size,input_size).zero_()#.cuda()
if P['sys/use cuda']:
    inputs = inputs.cuda()
#
############################
#
if P['TRAIN']:
    P['net/criterion!'] = nn.MSELoss()#.cuda()
    if P['sys/use cuda']:
        P['net/criterion!'] = P['net/criterion!'].cuda()

    P['net/optimizer!'] = torch.optim.Adadelta(P['net/net!'].parameters(),lr=initial_learning_rate)

    targets = torch.FloatTensor(batch_size,output_size).zero_()#.cuda()
    if P['sys/use cuda']:
        targets = targets.cuda()
#
############################
#

if False:
    bags = sggo("/media/karlzipser/rosbags/processed_26Aug18_14h16m09s/Mr_Blue_Back_25Aug18_17h02m58s/*.bag")
    for b in bags:
        unix(d2s('rosbag play',b))
if P['TRAIN']:
    processed_data_location = P['path/processed data location.']
    CS_('Starting training...',fname(__file__))
    if not os.path.exists(opj(processed_data_location,'weights')):
        os.makedirs(opj(processed_data_location,'weights'))
    if not os.path.exists(opj(processed_data_location,'P')):
        os.makedirs(opj(processed_data_location,'P'))



    def get_descriptive_filename():
        return d2p('fnn_model','in',len(P['net/input lst.']),'hid',P['net/hidden_size.'],'out',len(P['net/target lst.']),time_str())

    dfn = get_descriptive_filename()
    CS_(dfn)
    so(opj(processed_data_location,'P',dfn),P)


while P['ABORT'] == False:
    try:
        UI = {}
        for i in range(batch_size):
            UI[i] = np.random.randint(len(prepare_data.usable_indicies))

        #print 'F'
        for i in range(batch_size):
            if P['TRAIN']:
                D = prepare_data.get_input_output_data_(
                    prepare_data.L,
                    prepare_data.np.random.choice(prepare_data.usable_indicies),
                    #prepare_data.usable_indicies[UI[i]],
                    P)
                UI[i] += 1
                #print UI[i]
                if UI[i] > len(prepare_data.usable_indicies):
                    UI[i] = np.random.choice(prepare_data.usable_indicies)
            IO = {}
            io_list = ['input']
            if P['TRAIN']:
                io_list.append('target')
            for q in io_list:
                IO[q] = na([])
                for t in P['net/'+q+' lst.']:
                    if P['TRAIN']:
                        IO[q] = np.concatenate([IO[q],1.0*D[q][t]],axis=None)
                    else:
                        IO[q] = np.concatenate([IO[q],na(R[t]['vals'][-60:])],axis=None)
 
            inputs[i,:]=torch.from_numpy(IO['input'])
            if P['TRAIN']:
                targets[i,:]=torch.from_numpy(IO['target'])
        prepare_data.display_data3(D,P,title=d2s('batch',i))
#
############################
#            
        if P['TRAIN']:
            P['net/optimizer!'].zero_grad()

        P['net/outputs!'] = P['net/net!'](torch.autograd.Variable(inputs))

        if P['TRAIN']:
            P['net/loss!'] = P['net/criterion!'](P['net/outputs!'],torch.autograd.Variable(targets))
            P['net/loss!'].backward()
            nn.utils.clip_grad_norm(P['net/net!'].parameters(), 1.0)
            P['net/optimizer!'].step()
#
############################
#
            if epoch_timer__.check():
                spd2s(P['net/net!'])
                print 'epoch'
                P['path/weight out path'] = opj(processed_data_location,'weights',get_descriptive_filename()+'.pkl')
                spd2s(P['path/weight out path'])

                spd2s(P['net/net!'])
                torch.save(P['net/net!'].state_dict(),P['path/weight out path'])

                spd2s("torch.save(P['net/net!'].state_dict()",P['path/weight out path'],")")
                srpd2s("torch.save(P['net/net!'].state_dict()",P['path/weight out path'],")")
                CS_("torch.save(P['net/net!'].state_dict()",P['path/weight out path'],")")
                epoch_timer__.reset()
            if loss_timer__.check():
#
############################
#
                P['net/loss list!'].append(P['net/loss!'].data.cpu().numpy())
#
############################
#
                figure("P['net/loss!']")
                clf()
                plot(P['net/loss list!'],'.')
                spause()
                loss_timer__.reset()


        IO['output']= P['net/outputs!'][-1,:].data.cpu().numpy()
        if True:#target_output_timer__.check():
            figure(d2s('target output',P['net/batch size.']))
            clf()
            xylim(-11,11,-10,110)
            plot([-12,12],[49,49],'k')
            io_list = ['output']
            if P['TRAIN']:
                io_list.append('target')
            for io in io_list:
                if io == 'target':
                    c = '.:'
                else:
                    c = '.-'
                plot(range(-10,0),IO[io][:10],'r'+c)
                plot(range(0,10),IO[io][10:],'b'+c)
            spause()
            target_output_timer__.reset()
    except:
        exec(EXCEPT_STR)
raw_enter(__file__+' done. ')

"""
1) get flex net controlling blue car
2) get heading net conrolling car
3) experiment with acc as interference meter
"""
#EOF
