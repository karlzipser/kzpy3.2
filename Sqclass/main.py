# https://pytorch.org/hub/pytorch_vision_googlenet/
from kzpy3.vis3 import *
import torch
import torch.nn.utils as nnutils
from Sqclass.SqueezeNet_ldr_classifier_1024 import SqueezeNet
from kzpy3.Learn.clusters import Clusters

NUM_INPUT_CHANNELS = 3
INPUT_WIDTH = 41
INPUT_HEIGHT = 23
NUM_OUTPUTS = 1024
num_batches = 32

P= {}

C = Clusters()
cluster_list = C['cluster_list']
affinity=C['affinity']



def get_data_function(P):

    while True:
        a = rndint(1024)
        c = cluster_list[a]
        if len(c) > 25:
            break
        #print len(c)

    S = c[rndint(len(c))]

    r,i = S['name'],S['index']
    #print r,i
    #img = C['Runs'][r]['original_timestamp_data']['data']['left_image']['vals'][i]
    img = C['Runs'][r]['net_projections']['data']['normal'][i]
    #mci(img,scale=2)
    #img = cv2.resize(img,(INPUT_WIDTH,INPUT_HEIGHT))
    img = img.transpose(2,1,0)
    target = 1-affinity[a]
    #plot(target);spause()

    #clf();plot(target)
    return {
        'input':img,
        'target':target,
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




def save(N,losses,NETWORK_OUTPUT_FOLDER):
    print('saving net state . . .')
    weights = {'net':N.state_dict().copy()}
    for key in weights['net']:
        weights['net'][key] = weights['net'][key].cuda(0)
    net_str = 'net'+'_'+time_str()+'.'+str(losses[-1])
    net_str = net_str+'.cuda'
    os.system(d2s('mkdir -p',opj(NETWORK_OUTPUT_FOLDER,'weights')))
    os.system(d2s('mkdir -p',opj(NETWORK_OUTPUT_FOLDER,'loss')))
    torch.save(weights, opj(NETWORK_OUTPUT_FOLDER,'weights',net_str+'.infer'))
    so(losses,opj(NETWORK_OUTPUT_FOLDER,'loss',net_str+'.loss_avg'))
    print('. . . done saving.')



def __save(N,losses,NETWORK_OUTPUT_FOLDER):
    print('saving net state . . .')
    Net = {
        'weights':N.state_dict().copy(),
        'losses':losses,
        'clips':[],
    }
    for k in Net['weights']:
        Net['weights'][k] = Net['weights'][k].cuda(0)
    net_str = 'net'+'_'+time_str()+'.'+str(losses[-1])
    os.system(d2s('mkdir -p',opj(NETWORK_OUTPUT_FOLDER)))
    torch.save(Net, opj(NETWORK_OUTPUT_FOLDER,net_str+'.dic'))
    print('. . . done saving.')



def load(G,NETWORK_OUTPUT_FOLDER):
    f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'weights'),['.infer'],[])
    clp('Resuming with','`','',f,'','`--rb'); time.sleep(1)
    save_data = torch.load(f)
    G.load_state_dict(save_data['net'])
    f = most_recent_file_in_folder(opj(NETWORK_OUTPUT_FOLDER,'loss'),['.loss_avg.pkl'],[])
    losses = lo(f)
    return losses


if __name__ == '__main__':


    

    net_name = fname(pname(__file__))

    G = SqueezeNet().cuda()#(num_classes=NUM_OUTPUTS).cuda()
    optimizer = torch.optim.Adam(G.parameters(), lr=0.001, betas=(0.5, 0.999))
    #optimizer = torch.optim.Adadelta(filter(lambda p: p.requires_grad,G.parameters()))
    criterion = torch.nn.MSELoss().cuda()
    loss_list = []
    
    NETWORK_OUTPUT_FOLDER = opjD('Networks',net_name)

    if len(sggo(NETWORK_OUTPUT_FOLDER,'weights','*')) > 0:
        loss_list = load(G,NETWORK_OUTPUT_FOLDER)
    else:
        os.system(d2s('mkdir -p',NETWORK_OUTPUT_FOLDER))

    torch.cuda.set_device(0)

    if host_name != 'bdd4':
        CA()

    timer = Timer(30)
    save_timer = Timer(300)
    freq_timer = Timer(10)
    run_timer = Timer()
    cv_timer = Timer(0.1)

    while True:
        G.zero_grad()
        Data = make_batch(get_data_function,P,num_batches)
        #print shape(Data['input']),shape(Data['target'])
        x = G.forward(torch.from_numpy(Data['input']).cuda().float())
        target = torch.from_numpy(Data['target']).cuda().float()
        #print x.size(),target.size()
        loss = criterion(x,target)
        loss.backward()
        nnutils.clip_grad_norm(G.parameters(), 1)
        optimizer.step()
        loss_list.append(loss.data.cpu().numpy())


        if save_timer.check():
            save_timer.reset()
            save(G,loss_list,NETWORK_OUTPUT_FOLDER)

        #print Data['input'][:,0,0],Data['target'][:,0],dp(x[0,0].data.cpu().numpy()),dp(loss_list[-1])
        if cv_timer.check():
            cv_timer.reset()
            k = cv2.waitKey(1)

        if timer.check():
            timer.reset()
            #print loss_list[-1]
            if host_name != 'bdd4':
                figure('loss');clf();#ylim(0.02);
                plot(loss_list[100:],'.')#;spause()

                t = Data['target'][0,:]

                target_index = np.argmax(t)

                y=x.data.cpu().numpy()[0,:]

                q = len(y[y<y[target_index]])

                clp(1024-q,' ',int(100*q/1024.),'%',s0='')

                figure('target-output');clf();plt_square();xylim(0,1,0,1);plot(t,y,'.');plot([0,1],[0,1],'r')#;spause()
                y2=x.data.cpu().numpy()[6,:]
                figure('target-output2');clf();plt_square();xylim(0,1,0,1);plot(t,y2,'.');plot([0,1],[0,1],'r')#;spause()

                mi(Data['input'][0,:,:,:].transpose(2,1,0),'input 0');spause()
                mi(Data['input'][6,:,:,:].transpose(2,1,0),'input 6');spause()

        f = freq_timer.freq(do_print=False)
        if is_number(f):
            clp( 'Frequency =', int(np.round(f*num_batches)), 'Hz, run time =',format_seconds(run_timer.time()))











#EOF
