from kzpy3.vis3 import *

assert 'run_name' in Arguments
Defaults = {
    'start':0,
    'stop':-1,
    'start_percent':None,
    'stop_percent':None,
    'step':1,
    'scale':3.0,
    'show':True,
    'save':False,
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
read_path = opjD('Data','pts2D_multi_step','h5py',Arguments['run_name']+'.h5py')
save_path = read_path.replace('/h5py/','/h5py_half/')

if os.path.exists(save_path):
    clp('!!!',save_path,'exists!!!','`wrb')
    exit()

make_path_and_touch_file(save_path)

A = Arguments

clp('processing',Arguments['run_name'],'`--r')

F = h5r(read_path)

G = {'images':[],'index':[]}

a0,O,a1 = open_run2(Arguments['run_name'])

indicies = F['index'][:]

mx = len(F['images'])

if A['stop'] == -1:
    A['stop'] = mx

if A['start_percent'] is not None:
    A['start'] = int(A['start_percent'] * mx / 100.0)

if A['stop_percent'] is not None:
    A['stop'] = int(A['stop_percent'] * mx / 100.0)

assert A['stop'] > A['start']

cg(A['start'],A['stop'],A['step'])

for i in range(A['start'],A['stop'],A['step']):
    #print i

    G['index'].append(F['index'][i])
    
    img = F['images'][i][47-18:94-18,42:42+168/2,:]
    assert shape(img) == (47, 84, 3)
    img = cv2.resize(img,(0,0),fx=2.0,fy=2.0)
    assert shape(img) == (94, 168, 3)
    G['images'].append(img)

    if Arguments['show']:
        mci(O['left_image']['vals'][indicies[i]],title='a',scale=3.)
        mci(F['images'][i],title='b',scale=A['scale'],delay=1)
        mci(G['images'][-1],title='c',scale=A['scale'],delay=1)

F.close()

if Arguments['show']:
    raw_enter('Hit return to exit.')

G_ = h5w(save_path)
G_.create_dataset('index',data=na(G['index']))
G_.create_dataset('images',data=na(G['images']),dtype='uint8')          
G_.close()

exit()

#EOF
