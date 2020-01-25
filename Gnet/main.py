# https://pytorch.org/hub/pytorch_vision_googlenet/
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
from Gnet.googlenet import GoogLeNet
from kzpy3.Learn.clusters import Clusters

NUM_INPUT_CHANNELS = 3
INPUT_WIDTH = 224
INPUT_HEIGHT = 224
NUM_OUTPUTS = 1024
num_batches = 32

P= {}

C = Clusters()
cluster_list = C['cluster_list']
affinity=C['affinity']

if False:
    r = 'tegra-ubuntu_16Oct18_10h02m45s'
    i = 11598,
    pro = C['Runs'][r]['net_projections']['data']['normal']
    img = C['Runs'][r]['original_timestamp_data']['data']['left_image']['vals'][i]
    img = pro[i]

#input_template = zeros((NUM_INPUT_CHANNELS, INPUT_WIDTH, INPUT_HEIGHT))
#target_template = zeros(NUM_OUTPUTS)

def get_data_function(P):

    a = rndint(1024)
    c = cluster_list[a]
    S = c[rndint(len(c))]
    r,i = S['name'],S['index']
    #print r,i
    img = C['Runs'][r]['original_timestamp_data']['data']['left_image']['vals'][i]
    #mci(img,scale=2)
    img = cv2.resize(img,(224,224))
    img = img.transpose(2,1,0)
    target = affinity[a]
    #clf();plot(target)
    return {
        'input':img,
        'target':affinity[a],
        #'pro':C['Runs'][r]['net_projections']['data']['normal'][i]
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
    if False:
        G = GoogLeNet(num_classes=NUM_OUTPUTS).cuda()
        optimizer = torch.optim.Adam(G.parameters(), lr=0.01, betas=(0.5, 0.999))
        #optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,G.parameters()))
        criterion = torch.nn.MSELoss()
        loss_list = []
    



    timer = Timer(3000)
    CA()
    while True:
        G.zero_grad()
        Data = make_batch(get_data_function,P,num_batches)
        #print shape(Data['input']),shape(Data['target'])
        x = G.forward(torch.from_numpy(Data['input']).cuda().float())
        target = torch.from_numpy(Data['target']).cuda().float()
        loss = criterion(x,target)
        loss.backward()
        nnutils.clip_grad_norm(G.parameters(), 1)
        optimizer.step()
        loss_list.append(loss.data.cpu().numpy())

        #print Data['input'][:,0,0],Data['target'][:,0],dp(x[0,0].data.cpu().numpy()),dp(loss_list[-1])
        if timer.check():
            timer.reset()
            figure('loss');clf();plot(loss_list[100:],'.')#;spause()

            t = Data['target'][0,:]
            y=x.data.cpu().numpy()[0,:]
            figure('target-output');clf();plt_square();plot(t,y,'.')#;spause()

            mci(Data['input'][0,:,:,:].transpose(2,1,0),scale=2,title='input');spause()












#EOF
