from kzpy3.vis3 import *

assert 'run_name' in Arguments
Defaults = {
    'start':0,
    'stop':-1,
    'start_percent':None,
    'stop_percent':None,
    'step':1,
    'scale':3.0,
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]
save_path = opjD('Data','pts2D_multi_step','h5py',Arguments['run_name']+'.h5py')

A = Arguments


F = h5r(save_path)

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
    print i

    mci(O['left_image']['vals'][indicies[i]],title='a',scale=3.)

    mci(F['images'][i],title='b',scale=A['scale'],delay=1)


raw_enter('Hit return to exit.')

exit()

#EOF
