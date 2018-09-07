
from kzpy3.utils3 import *
import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable
from kzpy3.Train_app.OneD.Heading_fnn0.live_default_values import *
import roslib
import std_msgs.msg
import geometry_msgs.msg
import rospy
exec(identify_file_str)
try:
    ff = __file__
except:
    ff = '__file__'



for k in P:
    k_short_safe = k.split('/')[-1].replace(' ','_').replace(',','__').replace('.','').replace('!','')
    ex_str = d2n(k_short_safe,' = ',"P['",k,"']")
    print ex_str
    exec(ex_str)

torch.cuda.set_device(0)
torch.cuda.device(0)

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


flex_names = []
for fb in ['f','b']:
    for lr in ['l','r','c']:
        for i in [0,1]:
            flex_names.append(d2n('x',fb,lr,i))
flex_names.append('xan0')

for f in flex_names:
    s = """
def FLEX__callback(msg):
    R['FLEX']['ts'].append(time.time())
    R['FLEX']['vals'].append(msg.data)
rospy.Subscriber('/bair_car/FLEX', std_msgs.msg.Int32, callback=FLEX__callback)
    """
    exec_str = s.replace('FLEX',f)
    exec(exec_str)


###start
if CS('initalize network',s=ff):

    P['net/net!'] = Net(input_size, hidden_size, output_size).cuda()

    spd2s(P['net/net!'])

    if True:
        spd2s("P['cmd/resume from saved state.'] = True")
        latest_weights = '/home/karlzipser/kzpy3/Train_app/OneD/older/Train_fnn0/__local__/weights/fnn_model.01Sep18_08h54m04s.pkl'#most_recent_file_in_folder(P['path/weights file.'])
        saved_net = torch.load(latest_weights)
        P['net/net!'].load_state_dict(saved_net)
        spd2s(P['net/net!'])
        CS_(d2s('resuming with weight file',latest_weights),section=fname(__file__))
    else:#except:
        CS_(d2s('failed to load weights!'),section=fname(__file__),exception=True)
        exec(EXCEPT_STR)

    inputs = torch.FloatTensor(1,input_size).zero_().cuda()
###stop
    raw_enter()

if CS('run network live',__file__):

    while P['ABORT'] == False:
        IO = {}
        for q in ['input']:#,'target']:
            IO[q] = na([])
            for t in P['net/'+q+' lst.']:
                IO[q] = np.concatenate([IO[q],D[q][t]],axis=None)
        inputs[0,:] = torch.from_numpy(IO['input'])

        P['net/optimizer!'].zero_grad()
        P['net/outputs!'] = P['net/net!'](torch.autograd.Variable(inputs))

        IO['output']= P['net/outputs!'][-1,:].data.cpu().numpy()



"""
1) get flex net controlling blue car
2) get heading net conrolling car
"""
#EOF
