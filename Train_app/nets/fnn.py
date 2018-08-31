from kzpy3.utils3 import *
import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable

input_size = 60*8
hidden_size = 500
num_classes = 10
num_epochs = 50
batch_size = 100
learning_rate = 0.001


class Net(nn.Module):

    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


net = Net(input_size, hidden_size, num_classes)

# net.cuda()    # You can comment out this line to disable GPU

criterion = nn.MSELoss()
optimizer = torch.optim.Adadelta(net.parameters(),lr=learning_rate)

images = torch.FloatTensor(60*8).zero_()
labels = torch.FloatTensor(10).zero_()

for epoch in range(num_epochs):
	
	for i in range(batch_size):
		optimizer.zero_grad()
		outputs = net(images)
		loss = criterion(outputs, labels)
		loss.backward()
		optimizer.step()

	pd2s('Epoch',epoch,loss.data[0])


torch.save(net.state_dict(), 'fnn_model.pkl')


