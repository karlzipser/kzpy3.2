from kzpy3.vis import *
from Parameters import args
import kzpy3.teg9data.utils.Segment_Data as Segment_Data

hdf5_runs_path = args.data_path + '/hdf5/runs'
hdf5_segment_metadata_path = args.data_path + '/hdf5/segment_metadata'
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path, hdf5_runs_path)
        
class Data:

    class DataIndex:
        """
        Index object, keeps track of position in data stack.
        """
        def __init__(all_steer, ctr, epoch_counter):
            self.all_steer = all_steer
            self.ctr = ctr
            self.epoch_counter = epoch_counter

    def __init__(self):
        print('loading train_all_steer...')  # Loads pkl index file
        self.train_index = DataIndex(lo('/home/karlzipser/Desktop/' +
                                        'train_all_steer')), -1, 0)
        print('loading val_all_steer...')
        self.val_index = DataIndex(lo('/home/karlzipser/Desktop/' +
                                        'val_all_steer')), -1, 0)

    def get_data(self, run_code, seg_num, offset):
        data = Segment_Data.get_data(run_code, seg_num, offset,
                                     args.stride * args.nsteps, offset,
                                     args.nframes, ignore=args.ignore,
                                     require_one=args.require_one,
                                     use_states=args.use_states)
        return data

    def next(self, data_index):
        if data_index.ctr >= len(data_index.all_steer):
            data_index.ctr = -1
            data_index.epoch_counter += 1
        if data_index.ctr == -1:
            data_index.ctr = 0
            print('shuffle start')
            random.shuffle(data_index.all_steer)
            print('shuffle finished')
        data_index.ctr += 1
        return data_index.all_steer[data_index.ctr]
