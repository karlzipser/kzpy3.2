from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/pytorch1','kzpy3/pytorch1/train9'])
import Parameters as P
from vis2 import *
import torch




def Batch(d):
    batch_size = d['batch_size']

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
                #print('A')
                _data = get_data_function(get_data_args)
            data = _data
            #print('B')
            _data_into_batch(data)
            #print('C')
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

            metadata = torch.cat((zero_matrix, metadata), 1) # racing

            if data['desired_direction'] == 0: # caffe
                    metadata = torch.cat((zero_matrix, metadata), 1)
            else:
                metadata = torch.cat((one_matrix, metadata), 1)

            if data['behavioral_mode'] == 'Follow_Arena_Potential_Field':
                    metadata = torch.cat((one_matrix, metadata), 1) #follow
                    metadata = torch.cat((zero_matrix, metadata), 1) #direct
            else:
                metadata = torch.cat((zero_matrix, metadata), 1) #follow
                metadata = torch.cat((one_matrix, metadata), 1) #direct

            metadata = torch.cat((zero_matrix, metadata), 1) #play
            metadata = torch.cat((zero_matrix, metadata), 1) #furtive


            for i in range(122): # Concatenate zero matrices to fit the dataset
                metadata = torch.cat((zero_matrix, metadata), 1)
            D['metadata'] = torch.cat((metadata, D['metadata']), 0)


        if True:

            s = data['steer'].astype(float)#[-net.N_STEPS:]
            m = data['motor'].astype(float)#[-net.N_STEPS:]
            data['steer'] = ((0.0*m+1.0)*s).astype(float)
            if len(data['other_car_inverse_distances']) < 1:
                data['other_car_inverse_distances'] = np.zeros((11)).astype(float)
            steer = torch.from_numpy(data['steer'].astype(float)).cuda().float() / 99.
            motor = torch.from_numpy(data['motor'].astype(float)).cuda().float() / 99.
            marker_inverse_distances =  torch.from_numpy(data['marker_inverse_distances'].astype(float)).cuda().float()
            other_car_inverse_distances= torch.from_numpy(data['other_car_inverse_distances'].astype(float)).cuda().float()
            potential_values= torch.from_numpy(data['potential_values'].astype(float)).cuda().float()
            relative_heading= torch.from_numpy(np.array([data['relative_heading']]).astype(float)).cuda().float()
            velocity = torch.from_numpy(np.array([data['velocity']]).astype(float)).cuda().float()
            clock_potential_values = torch.from_numpy(data['clock_potential_values'].astype(float)).cuda().float()
            """
            #assert(len(data['steer'])==10)
            assert(np.shape(data['steer'])[0]==10)
            assert(np.shape(data['motor'])[0]==10)
            assert(np.shape(data['marker_inverse_distances'])[0]==11)
            assert(np.shape(data['other_car_inverse_distances'])[0]==11)
            assert(np.shape(data['potential_values'])[0]==11)
            assert(np.shape(data['relative_heading'])[0]==1)
            assert(np.shape(data['velocity'])[0]==1)
            assert(np.shape(data['clock_potential_values'])[0]==11)

            #assert(len(data[''])==11)
            #assert(len(data[''])==11)
            #assert(len(data[''])==11)
            #assert(len(data[''])==1)
            #assert(len(data[''])==1)
            #assert(len(data[''])==11)

            print steer
            print motor
            print marker_inverse_distances
            print other_car_inverse_distances
            print potential_values
            print relative_heading
            print velocity
            print clock_potential_values
            """


            target_data = torch.unsqueeze(torch.cat((steer,motor,marker_inverse_distances,other_car_inverse_distances,
                potential_values,relative_heading/360.0,velocity,clock_potential_values), 0), 0)
            D['target_data'] = torch.cat((target_data, D['target_data']), 0)

    def _clear():
        D['batch_size'] = None
        D['camera_data'] = None
        D['metadata'] = None
        D['target_data'] = None
        D['names'] = None
        D['outputs'] = None
        D['loss'] = None
    D['clear'] = _clear

    def _train(d):
        optimizer = d['optimizer']
        criterion = d['criterion']
        
        optimizer.zero_grad()
        D['outputs'] = D['net'](torch.autograd.Variable(D['camera_data']), torch.autograd.Variable(D['metadata'])).cuda()
        D['loss'] = criterion(D['outputs'], torch.autograd.Variable(D['target_data']))
        D['loss'].backward()
        optimizer.step()
    D['train'] = _train

    def _display(d):
        if 'print_now' not in d:
            d['print_now'] = False
        print_now = d['print_now']

        if P.print_timer.check() or print_now:

            #outputs = d['outputs']

            o = D['outputs'][0].data.cpu().numpy()
            #o = outputs[0].data.cpu().numpy()
            t= D['target_data'][0].cpu().numpy()
            print('1. Output:')
            print(t) # Output of Network
            print('2. Labels:')
            print(o)
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
            figure('steer')
            clf()
            ylim(-0.05,1.05);xlim(0,len(t))
            plot([-1,60],[0.49,0.49],'k');plot(o,'og'); plot(t,'or'); plt.title(D['names'][0])
            pause(0.000000001)
            P.print_timer.reset()
    D['display'] = _display

    return D
