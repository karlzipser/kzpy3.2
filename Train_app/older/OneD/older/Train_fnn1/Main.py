from kzpy3.vis3 import *
import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable
from prepare_data import *#from kzpy3.Train_app.Train_fnn1.prepare_data import *
exec(identify_file_str)


torch.cuda.set_device(P['GPU'])
torch.cuda.device(P['GPU'])

input_size = P['num_input_timesteps']*len(P['input_lst'])
hidden_size = P['hidden_size']#500
output_size = len(P['target_index_range'])*len(P['target_lst'])
num_epochs = 50
batch_size = P['batch_size']#100
learning_rate = 0.1


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


net = Net(input_size, hidden_size, output_size).cuda()
_random_weights = True
if P['resume from saved state']:
    try:
        latest_weights = most_recent_file_in_folder(opj(P['processed data location'],'weights'))
        saved_net = torch.load(latest_weights)
        net.load_state_dict(saved_net)
        CS_(d2s('resuming with weight file',latest_weights),section=fname(__file__))
        _random_weights = False
    except:
        CS_(d2s('failed to load weights!'),section=fname(__file__),exception=True)
        exec(EXCEPT_STR)
if _random_weights:
    CS_('training with random weights',fname(__file__))

criterion = nn.MSELoss().cuda()
optimizer = torch.optim.Adadelta(net.parameters(),lr=learning_rate)

inputs = torch.FloatTensor(batch_size,input_size).zero_().cuda()
targets = torch.FloatTensor(batch_size,output_size).zero_().cuda()

loss_timer = Timer(10)
epoch_timer = Timer(15*60)
target_output_timer = Timer(1)
loss_list = []
CS_('Starting training...',fname(__file__))
while True:
    if epoch_timer.check():
        print 'epoch'
        torch.save(net.state_dict(), opj(P['processed data location'],'weights',d2n('fnn_model.',time_str(),'.pkl')))
        epoch_timer.reset()
    if loss_timer.check():
        loss_list.append(loss.data.cpu().numpy())
        figure('loss')
        clf()
        plot(loss_list,'.')
        spause()
        loss_timer.reset()
    for i in range(batch_size):
        D = get_input_output_data(L,int(I['sig_sorted'][-np.random.randint(P['sig sorted value']),0]),P)
        IO = {}
        for q in ['input','target']:
            IO[q] = na([])
            for t in P[q+'_lst']:
                IO[q] = np.concatenate([IO[q],D[q][t]],axis=None)
        inputs[i,:]=torch.from_numpy(IO['input'])
        targets[i,:]=torch.from_numpy(IO['target'])

    optimizer.zero_grad()
    outputs = net(torch.autograd.Variable(inputs))
    loss = criterion(outputs,torch.autograd.Variable(targets))
    loss.backward()
    nn.utils.clip_grad_norm(net.parameters(), 1.0)
    optimizer.step()

    IO['output']= outputs[-1,:].data.cpu().numpy()
    if target_output_timer.check():
        figure('target output')
        clf()
        xylim(-11,11,-1,100)
        plot([-12,12],[49,49],'k')
        plot(range(-10,0),IO['target'][:10],'r.:')
        plot(range(-10,0),IO['output'][:10],'r.-')
        plot(range(0,10),IO['target'][10:],'b.:')
        plot(range(0,10),IO['output'][10:],'b.-')
        spause()
        target_output_timer.reset()



#EOF
