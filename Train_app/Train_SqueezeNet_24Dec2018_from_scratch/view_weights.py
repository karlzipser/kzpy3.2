from kzpy3.vis3 import *
import torch
import default_values
import Network_Module
_ = default_values.P

_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks',fname(_['project_path']))
_['INITIAL_WEIGHTS_FOLDER'] = opj(_['NETWORK_OUTPUT_FOLDER'],'weights')
_['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(_['INITIAL_WEIGHTS_FOLDER'],['.infer'],[])

Network = Network_Module.Pytorch_Network(_)
n = Network['net']

save_data = torch.load(_['WEIGHTS_FILE_PATH'])
n=save_data['net'] 

p = n['post_metadata_features.0.squeeze.weight'] 
q = p.cpu().numpy() 
q = q[:,:,0,0]

figure(_['WEIGHTS_FILE_PATH'].replace(opjh(),'')+' ')
plot([0,256],[0,0],'b-')
plot(q.transpose(1,0),'ko')
mi(q,_['WEIGHTS_FILE_PATH'].replace(opjh(),''))
raw_enter()

