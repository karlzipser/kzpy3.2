# https://pytorch.org/hub/pytorch_vision_googlenet/
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils

from Gnet.googlenet import GoogLeNet


NUM_INPUT_CHANNELS = 3
INPUT_WIDTH = 300
INPUT_HEIGHT = 300
NUM_OUTPUTS = 1000
P= {}

def get_data_function(P):

    a = random.choice([0,1])
    b = random.choice([0,1])
    n = 0#1/10.

    if a and b:
        c = 0
    elif a or b:
        c = 1
    else:
        c = 0

    input_data =  n*rndn(NUM_INPUT_CHANNELS, INPUT_WIDTH, INPUT_HEIGHT)
    input_data[0,:] += a
    input_data[1,:] += b

    target_data =   0*rndn(1,1000)
    target_data += c
    return {
        'input':input_data,
        'target':target_data,
    }


def make_batch(get_data_function,P,batch_size):
    Data = {}
    for i in range(batch_size):
        D = get_data_function(P)
        for k in D.keys():
            if k not in Data:
                Data[k] = []
            Data[k].append(D[k])
    for k in Data.keys():
        Data[k] = na(Data[k])
    return Data



if True:
    G = GoogLeNet() 
    optimizer = torch.optim.Adam(G.parameters(), lr=0.01, betas=(0.5, 0.999))
    #optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,G.parameters()))
    criterion = torch.nn.MSELoss()
    loss_list = []
    timer = Timer(5)
    while True:
        G.zero_grad()
        Data = get_data_function(P)
        x = G.forward(torch.from_numpy(na([Data['input']])).float())
        target = torch.from_numpy(Data['target']).float()
        loss = criterion(x,target)
        loss.backward()
        nnutils.clip_grad_norm(G.parameters(), 1)
        optimizer.step()
        loss_list.append(loss.data.cpu().numpy())

        print Data['input'][:,0,0],Data['target'][:,0],dp(x[0,0].data.cpu().numpy()),dp(loss_list[-1])
        if timer.check():
            timer.reset()
            clf();plot(loss_list,'.');spause()

#EOF
