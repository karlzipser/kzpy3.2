import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import argparse
import os
import tqdm
import scipy.ndimage as nd
#from utils import deprocess, preprocess, clip
from kzpy3.vis3 import *
from Gnet.googlenet import GoogLeNet
NUM_OUTPUTS = 1024


path = opjD('Destkop_clusters_and_not_essential_24July2019')
affinity = lo(opj(path,'affinity'))

import numpy as np
import torch
from torchvision import transforms

mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])

preprocess = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])


def deprocess(image_np):
    image_np = image_np.squeeze().transpose(1, 2, 0)
    image_np = image_np * std.reshape((1, 1, 3)) + mean.reshape((1, 1, 3))
    image_np = np.clip(image_np, 0.0, 255.0)
    return image_np


def clip(image_tensor):
    for c in range(3):
        m, s = mean[c], std[c]
        image_tensor[0, c] = torch.clamp(image_tensor[0, c], -m / s, (1 - m) / s)
    return image_tensor

out_sum = zeros(1024)



Images = {}
max_images = 10

def dream(image, model, iterations, lr):
    global out_sum
    """ Updates the image to maximize outputs for n iterations """
    #Tensor = torch.cuda.FloatTensor if torch.cuda.is_available else torch.FloatTensor
    #Tensor =  torch.FloatTensor
    Tensor = torch.cuda.FloatTensor
    image = Variable(Tensor(image), requires_grad=True)
    
    target = torch.from_numpy((1-affinity[400])**2).cuda().float()
    #target = torch.from_numpy(zeros((1024))).cuda().float() + 1
    #target[400] = 0

    criterion = torch.nn.MSELoss().cuda()

    for i in range(iterations):
        #print(i)`
        model.zero_grad()
        out = model(image)
        #print(target.size())
        #print(out.size())
        out_sum = out.data.data.cpu().numpy()[0,:]
        #cc = np.corrcoef(out_sum,1-affinity[400])[0,1]
        cc = 1.
        if cc < 0:
            cc = 0
        #figure(1);clf();plot(out_sum,'.');spause();raw_enter()
        #plot(target.data.numpy(),'o')
        #plot(out.data.numpy()[0,:],'.');spause()
        loss = criterion(out,target)
        #out[0,400]=1
        #print(out.size())
        #loss = out.norm()
        #loss[:]=0
        #loss[400]=1
        #print(loss)
        #print(loss.size())
        loss.backward()
        avg_grad = np.abs(image.grad.data.cpu().numpy()).mean()
        norm_lr = lr / avg_grad
        image.data = (1-lr/10.)*image.data + cc * norm_lr * image.grad.data 
        image.data = clip(image.data)
        image.grad.data.zero_()

        return_image = image.cpu().data.numpy()

        loss_val = float(loss.cpu().data.numpy())
        #kprint(loss_val,type(loss_val))

        if len(Images) < 1:
            Images[loss_val] = return_image

        elif loss_val < min(Images):
            Images[loss_val] = return_image

        if len(Images) > max_images:
            a = sorted(Images)
            for b in range(max_images,len(Images)):
                del Images[b]

    return an_element(Images)
    #return return_image #img_list[rndint(len(img_list))] #

timer = Timer(1)
deprocessed_dreamed_image = None



def deep_dream(image, model, iterations, lr, octave_scale, num_octaves):
    """ Main deep dream method """
    global deprocessed_dreamed_image
    image = preprocess(image).unsqueeze(0).cpu().data.numpy()

    # Extract image representations for each octave
    octaves = [image]
    for _ in range(num_octaves - 1):
        octaves.append(nd.zoom(octaves[-1], (1, 1, 1 / octave_scale, 1 / octave_scale), order=1))

    detail = np.zeros_like(octaves[-1])
    for i in range(100000):
        lr *= 0.99999
        print(lr)
        for octave, octave_base in enumerate(tqdm.tqdm(octaves[::-1], desc="Dreaming")):
            if octave > 0:
                # Upsample detail to new octave dimension
                detail = nd.zoom(detail, np.array(octave_base.shape) / np.array(detail.shape), order=1)
            # Add deep dream detail from previous octave to new base
            input_image = octave_base + detail
            # Get new deep dream image
            dreamed_image = dream(input_image, model, iterations, lr)
            #dreamed_image += 0.1*torch.randn(1,3,244,244)
            # Extract deep dream details
            detail = dreamed_image - octave_base
            if timer.check():
                timer.reset()
                figure(8);clf()
                plt_square()
                xylim(-.5,1.5,-.5,1.5)
                
                plot(1-affinity[400],1-out_sum/out_sum.max(),'.');plot([0,1],[0,1],'r')
                #xylim(0,1,-3,-10)
                #figure(9);clf()
                #plot(1-affinity[400],1-out_sum,'.')#;plot([0,1],[0,1],'r')
                #spause()
                mi(deprocess(dreamed_image),2)
                spause()
            deprocessed_dreamed_image = deprocess(dreamed_image)
    return deprocess(dreamed_image)





"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_image", type=str, default="images/supermarket.jpg", help="path to input image")
    parser.add_argument("--iterations", default=20, help="number of gradient ascent steps per octave")
    parser.add_argument("--at_layer", default=27, type=int, help="layer at which we modify image to maximize outputs")
    parser.add_argument("--lr", default=0.01, help="learning rate")
    parser.add_argument("--octave_scale", default=1.4, help="image scale between octaves")
    parser.add_argument("--num_octaves", default=10, help="number of octaves")
    args = parser.parse_args()

    # Load image
    image = Image.open(args.input_image)

    # Define the model
    network = models.vgg19(pretrained=True)
    layers = list(network.features.children())
    model = nn.Sequential(*layers[: (args.at_layer + 1)])
    if torch.cuda.is_available:
        model = model.cuda()
    print(network)

    # Extract deep dream image
    dreamed_image = deep_dream(
        image,
        model,
        iterations=args.iterations,
        lr=args.lr,
        octave_scale=args.octave_scale,
        num_octaves=args.num_octaves,
    )

    # Save and plot image
    os.makedirs("outputs", exist_ok=True)
    filename = args.input_image.split("/")[-1]
    plt.figure(figsize=(20, 20))
    plt.imshow(dreamed_image)
    plt.imsave("outputs/output_{filename}", dreamed_image)
    plt.show()

"""
def load(G,NETWORK_OUTPUT_FOLDER):
    f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
    clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
    save_data = torch.load(f)
    G.load_state_dict(save_data['net'])
    f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
    losses = lo(f)
    return losses

if True:
    if True:
        G = GoogLeNet(num_classes=NUM_OUTPUTS).cuda()
        optimizer = torch.optim.Adam(G.parameters(), lr=0.001, betas=(0.5, 0.999))
        #optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,G.parameters()))
        criterion = torch.nn.MSELoss().cuda()
        loss_list = []
    
    loss_list = load(G,opjD('Networks/googlenet0'))

    b = deep_dream(rnd((244,244,3)), G, iterations=100, lr=.1, octave_scale=1, num_octaves=1)

#EOF

