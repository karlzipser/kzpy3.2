if '__file__' not in locals():
    __file__ = 'Data.py'
from kzpy3.utils2 import *
cprint('****************** '+__file__+' ******************','yellow')
pythonpaths(['kzpy3','kzpy3/teg9','kzpy3/pytorch2/Train_SqueezeNet'])
from kzpy3.vis import *
import Parameters as P
import data.utils.Segment_Data as Segment_Data

hdf5_runs_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/runs')
hdf5_segment_metadata_path = opj(P.BAIR_CAR_DATA_PATH,'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)
        
def Data():
    True
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
    D['train']['all_steer'] = lo(opjD('train_all_steer'))
    D['train']['ctr'] = -1
    D['val'] = {}
    print('loading val_all_steer...')
    D['val']['all_steer'] = lo(opjD('val_all_steer'))
    D['val']['ctr'] = -1
    print('...done loading.')
    D['train']['epoch_counter'] = 0
    D['val']['epoch_counter'] = 0
    def _next(d):
        mode = d['mode']
        True
        if D[mode]['ctr'] >= len(D[mode]['all_steer']):
            D[mode]['ctr'] = -1
            D[mode]['epoch_counter'] += 1
        if D[mode]['ctr'] == -1:
            D[mode]['ctr'] = 0
            print('shuffle start')
            random.shuffle(D[mode]['all_steer'])
            print('shuffle finished')
        steer = D[mode]['all_steer'][D[mode]['ctr']]
        D[mode]['ctr'] += 1
        return steer
    D['next'] = _next

    return D



#EOF