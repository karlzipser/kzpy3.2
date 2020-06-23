# https://gist.github.com/user01/68514db1127eb007f24d28bfd11dd60e
#,a
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Function

EPOCHS_TO_TRAIN = 5000000


NH = 40

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(2, NH, True)
        self.fc2 = nn.Linear(NH, 1, True)
        self.A = {}

    def forward(self, x):
        x = F.sigmoid(self.fc1(x))
        self.A['fc1_sum'] = torch.sum(torch.abs(x))
        self.A['fc1'] = x
        #inpt, = x.saved_variables
        #grad_input = inpt.clone().sign().mul(0.1)
        #grad_input += grad_output

        #x = L1Penalty.apply(x,0.1)

        x = self.fc2(x)

        return x


net = Net()

inputs = list(map(lambda s: Variable(torch.Tensor([s])), na([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]]) + rndn(4,2)
))
targets = list(map(lambda s: Variable(torch.Tensor([s])), [
    [0],
    [1],
    [1],
    [0]
]))


criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.01)

sparse_list, loss_list = [],[]

figure(3)
clf()

for idx in range(0, EPOCHS_TO_TRAIN):
    inputs = list(map(lambda s: Variable(torch.Tensor([s])), na([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]]) + 0.33*rndn(4,2)
    ))
    for input, target in zip(inputs, targets):
        optimizer.zero_grad()   # zero the gradient buffers
        output = net(input)
        regularization_loss = 0
        ctr = 0
        for param in net.parameters():
            #print(ctr,param)
            if ctr == 1:#ctr == 1:
                regularization_loss += torch.sum(torch.abs(param))
            ctr +=1
        loss = criterion(output, target) + 10 * regularization_loss
        loss.backward()
        optimizer.step()    # Does the update
    if idx % 1000 == 0:
        print(net.A['fc1'],regularization_loss)
        print("Epoch {: >8} Loss: {}".format(idx, loss.data.numpy()[0]))

        figure(3);clf()
        
        d = net.A['fc1'].data.numpy()[0]
        d = d / d.max()
        sparsity = np.sum(d)/len(d)
        print sparsity
        
        for input, target in zip(inputs, targets):
            plot(net.A['fc1'].data.numpy()[0])
            output = net(input)
            print("Input:[{},{}] Target:[{}] Predicted:[{}] Error:[{}]".format(
                int(input.data.numpy()[0][0]),
                int(input.data.numpy()[0][1]),
                int(target.data.numpy()[0]),
                round(float(output.data.numpy()[0]), 4),
                round(float(abs(target.data.numpy()[0] - output.data.numpy()[0])), 4)
            ))
        loss_list.append(loss.data.numpy()[0])
        sparse_list.append(sparsity)
        figure(5);clf();plot(loss_list)
        figure(6);clf();plot(sparse_list)
        spause()

print("")
print("Final results:")
for input, target in zip(inputs, targets):
    output = net(input)
    print("Input:[{},{}] Target:[{}] Predicted:[{}] Error:[{}]".format(
        int(input.data.numpy()[0][0]),
        int(input.data.numpy()[0][1]),
        int(target.data.numpy()[0]),
        round(float(output.data.numpy()[0]), 4),
        round(float(abs(target.data.numpy()[0] - output.data.numpy()[0])), 4)
    ))


#,b

#EOF