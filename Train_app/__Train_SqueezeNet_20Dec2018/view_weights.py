from kzpy3.vis3 import *
import torch
import kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.Network_Module as Network_Module
Network = Network_Module.Pytorch_Network()
n=Network['net'] 
#save_data = torch.load('/home/karlzipser/Desktop/Networks/_net_15Sept2018_1Nov_with_reverse_/weights/net_11Dec18_23h35m53s.infer') 
#save_data = torch.load('/home/karlzipser/Desktop/Networks/net_15Sept2018_1Nov_with_reverse_with_12imgs/weights/net_17Dec18_15h32m44s.infer') 
save_data = torch.load(most_recent_file_in_folder('/home/karlzipser/Desktop/Networks/net_15Sept2018_1Nov_with_reverse_with_12imgs/weights'))
n=save_data['net'] 
p = n['post_metadata_features.0.squeeze.weight'] 
q = p.cpu().numpy() 
q = q[:,:,0,0] 
q[:,128]/=10.
#mi(q[:,:129])  
mi(q,5)
raw_enter()

