from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/pytorch1'])
from vis2 import *
import torch
import torch.nn.utils as nnutils
print_timer = Timer(5)
img_saver = Image_to_Folder_Saver({'path':opjD('cameras0')})


def Batch(d):
    batch_size = d['batch_size']
    True
    D = {}
    D['net'] = d['net']
    D['type'] = 'batch'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','object to collect data for pytorch batch')
    D['batch_size'] = batch_size
    D['camera_data'] = torch.FloatTensor().cuda()
    D['metadata'] = torch.FloatTensor().cuda()
    D['target_data'] = torch.FloatTensor().cuda()
    D['names'] = []

    def _fill(d):
        get_data_function = d['get_data_function']
        get_data_args = d['get_data_args']

        for b in range(D['batch_size']):
            _data = None
            while _data == None:
                _data = get_data_function(get_data_args)
            data = _data
            _data_into_batch(data)
    D['fill'] = _fill

    def _data_into_batch(data):
        if True:
            D['names'].insert(0,data['name']) # This to match torch.cat use below

        if True:
            list_camera_input = []
            for t in range(D['net'].N_FRAMES):
                for camera in ('left', 'right'):
                    list_camera_input.append(torch.from_numpy(data[camera][t]))
            camera_data = torch.cat(list_camera_input, 2)
            camera_data = camera_data.cuda().float()
            camera_data = torch.transpose(camera_data, 0, 2)
            camera_data = torch.transpose(camera_data, 1, 2)
            D['camera_data'] = torch.cat((torch.unsqueeze(camera_data, 0), D['camera_data']), 0)

        if True:
            metadata = torch.FloatTensor().cuda()
            zero_matrix = torch.FloatTensor(1, 1, 23, 41).zero_().cuda()
            one_matrix = torch.FloatTensor(1, 1, 23, 41).fill_(1).cuda()
            for cur_label in ['racing', 'caffe', 'follow', 'direct', 'play', 'furtive']:
                if cur_label == 'caffe':
                    if data['states'][0]:
                        metadata = torch.cat((one_matrix, metadata), 1)
                    else:
                        metadata = torch.cat((zero_matrix, metadata), 1)
                else:
                    if data['labels'][cur_label]:
                        metadata = torch.cat((one_matrix, metadata), 1)
                    else:
                        metadata = torch.cat((zero_matrix, metadata), 1)

            for i in range(122): # Concatenate zero matrices to fit the dataset
                metadata = torch.cat((zero_matrix, metadata), 1)
            D['metadata'] = torch.cat((metadata, D['metadata']), 0)

        if True:
            s = data['steer']#[-net.N_STEPS:]
            m = data['motor']#[-net.N_STEPS:]
            r = range(2,31,3)
            s = array(s)[r]
            m = array(m)[r]
            steer = torch.from_numpy(s).cuda().float() / 99.
            motor = torch.from_numpy(m).cuda().float() / 99.
            target_data = torch.unsqueeze(torch.cat((steer, motor), 0), 0)
            D['target_data'] = torch.cat((target_data, D['target_data']), 0)

    def _clear():
        #D['batch_size'] = None
        #D['camera_data'] = None
        #D['metadata'] = None
        #D['target_data'] = None
        #D['names'] = None
        D['camera_data'] = torch.FloatTensor().cuda()
        D['metadata'] = torch.FloatTensor().cuda()
        D['target_data'] = torch.FloatTensor().cuda()
        D['names'] = []
        D['outputs'] = None
        D['loss'] = None
    D['clear'] = _clear


    def _forward(d):
        optimizer = d['optimizer']
        criterion = d['criterion']
        True
        optimizer.zero_grad()
        D['outputs'] = D['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
        D['loss'] = criterion(D['outputs'], torch.autograd.Variable(D['target_data']))
    D['forward'] = _forward

    def _backward(d):
        optimizer = d['optimizer']
        True
        D['loss'].backward()
        nnutils.clip_grad_norm(D['net'].parameters(), 1.0)
        optimizer.step()
    D['backward'] = _backward

    def _display(d):
        if 'print_now' not in d:
            d['print_now'] = False
        print_now = d['print_now']
        True
        if print_timer.check() or print_now:

            #outputs = d['outputs']

            o = D['outputs'][0].data.cpu().numpy()
            #o = outputs[0].data.cpu().numpy()
            t= D['target_data'][0].cpu().numpy()
            """
            print('1. Output:')
            print(o) # Output of Network
            print('2. Labels:')
            print(t)
            """
            print('3. Loss:')

            #print(array(loss_list[-loss_list_N:]).mean())
            #print(loss_list[-1])
            a=D['camera_data'][0][:].cpu().numpy()
            b=a.transpose(1,2,0)
            h = shape(a)[1]
            w = shape(a)[2]
            c = zeros((10+h*2,10+2*w,3))
            c[:h,:w,:] = z2o(b[:,:,3:6])
            c[:h,-w:,:] = z2o(b[:,:,:3])
            c[-h:,:w,:] = z2o(b[:,:,9:12])
            c[-h:,-w:,:] = z2o(b[:,:,6:9])
            mi(c,'cameras')
            img_saver['save']({'img':c})
            figure('steer')
            clf()
            ylim(-0.05,1.05);xlim(0,len(t))
            plot([-1,60],[0.49,0.49],'k');plot(o,'og'); plot(t,'or'); plt.title(D['names'][0])
            pause(0.000000001)
            print_timer.reset()
    D['display'] = _display

    return D
