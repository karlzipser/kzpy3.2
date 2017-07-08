if '__file__' not in locals():
    __file__ = 'Data.py'
from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch3/Train_SqueezeNet'])
from kzpy3.vis import *
import Parameters as P
import data.utils.Segment_Data as Segment_Data

hdf5_runs_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)

def Data():
    True
    train__run_seg_off_h5f = h5py.File(opjh(P.WORK_PATH,'train__run_seg_off.hdf5'),'r')
    val__run_seg_off_h5f = h5py.File(opjh(P.WORK_PATH,'val__run_seg_off.hdf5'),'r')
    D = {}
    D['type'] = 'Training_Data'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Object to hold various data and information for training')
    D['train_los_dic'] = {}

    def _get_data(d):
        run_code = d['run_code']
        seg_num = d['seg_num']
        offset = d['offset']
        True   
        data = Segment_Data.get_data(run_code,seg_num,offset,P.STRIDE*P.N_STEPS,offset+0,P.N_FRAMES,ignore=P.IGNORE,require_one=P.REQUIRE_ONE,use_states=P.USE_STATES)
        return data
    D['get_data'] = _get_data
    D['train'] = {}
    print('loading train_all_steer...')
    D['train']['run_seg_off'] = train__run_seg_off_h5f['data']
    D['train']['ctr'] = -1
    D['val'] = {}
    print('loading val_all_steer...')
    D['val']['run_seg_off'] = val__run_seg_off_h5f['data']
    D['val']['ctr'] = -1
    print('...done loading.')
    D['train']['epoch_counter'] = 0
    D['val']['epoch_counter'] = 0
    def _next(d):
        mode = d['mode']
        True
        if D[mode]['ctr'] >= len(D[mode]['run_seg_off']):
            D[mode]['ctr'] = -1
            D[mode]['epoch_counter'] += 1
        if D[mode]['ctr'] == -1:
            D[mode]['ctr'] = 0
            print('shuffle start')
            random.shuffle(D[mode]['run_seg_off'])
            print('shuffle finished')
        run_seg_off = D[mode]['run_seg_off'][D[mode]['ctr']]
        D[mode]['ctr'] += 1
        return run_seg_off
    D['next'] = _next

    return D





if False:
    DD = Data()
    run_seg_off = {}
    
    for mode in ['train','val']:
        run_seg_off[mode] = []
        for e in DD[mode]['run_seg_off']:
            f = [e[3],e[0],e[1]]
            run_seg_off[mode].append(f)
        run_seg_off[mode] = array(run_seg_off[mode])
        with h5py.File(opjD(mode+'__run_seg_off.hdf5'),'w') as h5f:
            h5f.create_dataset('data',data=run_seg_off[mode])


    with h5py.File(opjD('train__run_seg_off.hdf5'),'r') as h5f:
        b = h5f['data'][:]


def h5py_save_dataset(d):
    data = d['data']
    path = d['path']
    if 'name' in d:
        name = d['name']
    else:
        name = 'data'
    True
    with h5py.File(path,'w') as h5f:
        h5f.create_dataset(name,data=data)
def h5py_read_dataset(d):
    path = d['path']
    if 'name' in d:
        name = d['name']
    else:
        name = 'data'
    True
    with h5py.File(path,'r') as h5f:
        b = h5f[name][:]
    return b

#EOF