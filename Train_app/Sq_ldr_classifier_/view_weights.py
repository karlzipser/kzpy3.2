from kzpy3.vis3 import *
import torch
import default_values
import Network_Module
_ = default_values.P

print Arguments
_['NETWORK_OUTPUT_FOLDER'] = opjD('Networks',fname(_['project_path']))
_['INITIAL_WEIGHTS_FOLDER'] = opj(_['NETWORK_OUTPUT_FOLDER'],'weights')
_['WEIGHTS_FILE_PATH'] = most_recent_file_in_folder(_['INITIAL_WEIGHTS_FOLDER'],['.infer'],[])

if 'path' in Arguments:
    _['WEIGHTS_FILE_PATH'] = Arguments['path']


if False:
    _['WEIGHTS_FILE_PATH'] = opjD('Networks/net_24Dec2018_12imgs_projections/weights/net_25Dec18_20h12m56s.infer')#opjD('temp')

Network = Network_Module.Pytorch_Network(_)
n = Network['net']

save_data = torch.load(_['WEIGHTS_FILE_PATH'])
n=save_data['net'] 
figsize=(40,6)
p = n['post_metadata_features.0.squeeze.weight'] 
q = p.cpu().numpy() 
q = q[:,:,0,0] 
#q[:,128]/=10.
q[q>1]=1
q[q<-1]=-1
cr('*** note, q[q>1]=1, +/- ***')
figure(_['WEIGHTS_FILE_PATH'].replace(opjh(),'')+' ',figsize=figsize)
plot([0,256],[0,0],'b-')

w = q.transpose(1,0)
for i in range(len(w)):
    c = 'c.'
    if i in [128+4+13,128+4+14,128+4+15]:
        c = 'bo'
    if i in [128+1,128+2,128+3,128+4]:
        c = 'go'
    if i in [128]:
        c = 'ro'
    plot(zeros(16)+i,w[i,:],c)
figname = _['WEIGHTS_FILE_PATH'].replace(opjh(),'')
figure(figname,figsize=figsize)
mi(q,figname)
raw_enter()

