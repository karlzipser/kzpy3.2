
from kzpy3.vis import *
CS_('''
*** Look at the progress of training person_clothing_bigger_18Sept2015 ***
This network has conv1 four times bigger and conv2 two times bigger
''')

def vis_square(data, fig_name='vis_square',subplot_array=[1,1,1], padsize=1, padval=0):
    data -= data.min()
    data /= data.max()   
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    mi(data,fig_name,subplot_array)
    return data




 
for current_model in ['bvlc_googlenet_person','person_clothing_bigger_18Sept2015']:




	CS_('''training loss''')
	if current_model == 'person_clothing_bigger_18Sept2015':
		ns = txt_file_to_list_of_strings(opjh('caffe/models/'+current_model+'/slurm-434550.out'))
		ns += txt_file_to_list_of_strings(opjh('caffe/models/'+current_model+'/slurm-434875.out'))
	if current_model == 'bvlc_googlenet_person':
		ns = txt_file_to_list_of_strings(opjh('caffe/models/bvlc_googlenet_person/slurm-435348.out'))
		ns += txt_file_to_list_of_strings(opjh('caffe/models/bvlc_googlenet_person/slurm-435350.out'))

	PP[FF]=4,2
	plt.figure(d2n(current_model,''': loss'''))

	if current_model == 'bvlc_googlenet_person':
		st = 'Train net output #0: loss1/loss1 = '
		train_loss = []
		for n in ns:
		    if st in n:
		        train_loss.append(float(n.split(st)[1].split()[0]))
		plot(train_loss[1:],'.');

		st = 'Train net output #1: loss2/loss1 = '
		train_loss = []
		for n in ns:
		    if st in n:
		        train_loss.append(float(n.split(st)[1].split()[0]))
		plot(train_loss[1:],'.');

		st = 'Train net output #2: loss3/loss3 = '
		train_loss = []
		for n in ns:
		    if st in n:
		        train_loss.append(float(n.split(st)[1].split()[0]))
		plot(train_loss[1:],'.');

	if current_model == 'person_clothing_bigger_18Sept2015':
		ns = txt_file_to_list_of_strings(opjh('caffe/models/person_clothing_17Sept2015/slurm-434496.out'))
		ns += txt_file_to_list_of_strings(opjh('caffe/models/person_clothing_17Sept2015/slurm-434524.out'))
		ns += txt_file_to_list_of_strings(opjh('caffe/models/person_clothing_17Sept2015/slurm-434874.out'))
		st = 'Train net output #0: loss = '
		train_loss = []
		for n in ns:
		    if st in n:
		        train_loss.append(float(n.split(st)[1].split()[0]))
		plot(train_loss,'.');

		ns = txt_file_to_list_of_strings(opjh('caffe/models/person_clothing_bigger_18Sept2015/slurm-434550.out'))
		ns += txt_file_to_list_of_strings(opjh('caffe/models/person_clothing_bigger_18Sept2015/slurm-434875.out'))

		st = 'Train net output #0: loss = '
		train_loss = []
		for n in ns:
		    if st in n:
		        train_loss.append(float(n.split(st)[1].split()[0]))
		plot(train_loss,'.');	







	# Make sure that caffe is on the python path:
	caffe_root = opjh('caffe')  # this file is expected to be in {caffe_root}/examples
	import sys
	sys.path.insert(0, caffe_root + 'python')

	import caffe
	caffe.set_mode_cpu()

	model_to_load = False
	cms = gg(opjh('caffe/models/'+current_model+'/*.caffemodel'))
	if len(cms) > 0:
	    ctimes = []
	    for c in cms:
	        ctimes.append(os.path.getctime(c))
	    cms = sorted(cms,key=natural_keys)
	    ctimes = []
	    for c in cms:
	        ctimes.append(os.path.getctime(c))
	    sorted_indicies = np.argsort(np.array(ctimes))
	    model_to_load = cms[sorted_indicies[-1]]
	    print(d2s('***** model to load =',model_to_load))


	net = caffe.Net(opjh('caffe/models/'+current_model+'/deploy.prototxt'),model_to_load, caffe.TEST)

	#net = caffe.Net(opjh('caffe/models/bvlc_reference_caffenet/deploy.prototxt'),
	#                opjh('caffe/models/bvlc_reference_caffenet/model.caffemodel' ), #'caffe/models/bvlc_reference_caffenet/model.caffemodel'),
	#                caffe.TEST)











	CS_('''Latest weights.''')
	if current_model == 'person_clothing_bigger_18Sept2015':
		filters_b = net.params['conv1'][0].data.copy()
		PP[FF] = 8,4
	if current_model == 'bvlc_googlenet_person':
		filters_b = net.params['conv1/7x7_s2'][0].data.copy()
		PP[FF] = 4,2


	vis_square(filters_b.transpose(0, 2, 3, 1)[:,:,:,:],d2n(current_model,''': latest weights.'''),[1,2,1])
	f = filters_b.copy()

	for i in range(shape(f)[0]):
	    f[i,:,:,:] = z2o(f[i,:,:,:])
	vis_square(f.transpose(0, 2, 3, 1),d2n(current_model,''': latest weights.'''),[1,2,2]);
	model_to_load