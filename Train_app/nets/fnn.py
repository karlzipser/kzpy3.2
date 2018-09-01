from kzpy3.vis3 import *
import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable

from kzpy3.Train_app.Train_Z1dconvnet0.prepare_data import *
input_size = P['num_input_timesteps']*len(P['input_lst'])
hidden_size = 500
output_size = len(P['target_index_range'])*len(P['target_lst'])
num_epochs = 50
batch_size = 100
learning_rate = 0.001


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


net = Net(input_size, hidden_size, output_size)

#net.cuda()    # You can comment out this line to disable GPU

criterion = nn.MSELoss()
optimizer = torch.optim.Adadelta(net.parameters(),lr=learning_rate)

inputs = torch.FloatTensor(batch_size,input_size).zero_()
targets = torch.FloatTensor(batch_size,output_size).zero_()


#the_input = torch.FloatTensor(num_minibatches,num_topics,num_input_timesteps).zero_().cuda()
#the_target = torch.FloatTensor(num_minibatches,20,1).zero_().cuda()


loss_timer = Timer(10)
epoch_timer = Timer(15*60)
loss_list = []
CS_('Starting training...')
while True:
    if epoch_timer.check():
        print 'epoch'
        torch.save(net.state_dict(), 'fnn_model.pkl')
        epoch_timer.reset()
    if loss_timer.check():
        loss_list.append(loss.data.numpy())
        CA()
        plot(loss_list,'.')
        spause()
        loss_timer.reset()
    for i in range(batch_size):
        D = get_input_output_data(L,int(I['sig_sorted'][-np.random.randint(20000),0]),P)
        IO = {}
        for q in ['input','target']:
            IO[q] = na([])
            for t in P[q+'_lst']:
                IO[q] = np.concatenate([IO[q],D[q][t]],axis=None)
        #print shape(IO['input']),shape(inputs)
        inputs[i,:]=torch.from_numpy(IO['input'])
        targets[i,:]=torch.from_numpy(IO['target'])
    optimizer.zero_grad()
    outputs = net(torch.autograd.Variable(inputs))
    loss = criterion(outputs,torch.autograd.Variable(targets))
    loss.backward()
    nn.utils.clip_grad_norm(net.parameters(), 1.0)
    optimizer.step()




