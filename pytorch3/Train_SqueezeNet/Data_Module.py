from Parameters_Module import *
exec(identify_file_str)
import data.utils.Segment_Data as Segment_Data

hdf5_runs_path = opj(P['BAIR_CAR_DATA_PATH'],'hdf5/runs')
hdf5_segment_metadata_path = opj(P['BAIR_CAR_DATA_PATH'],'hdf5/segment_metadata')
Segment_Data.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path);print('.')

_ = dictionary_access
    
def Training_Data():
    D = {}
    True
    _(D,dic_type,equals,'Training_Data')
    _(D,purpose,equals,d2s(inspect.stack()[0][3],':','Object to hold various data and information for training'))
    _(D,train, equals, {})
    print('loading train_all_steer...')
    #_(D,train,all_data_moment_id_codes, equals, lo(opj(P[BAIR_CAR_DATA_PATH],'train_all_steer')))
    D[train][all_data_moment_id_codes] = lo(opj(P[BAIR_CAR_DATA_PATH],'train_all_steer'))
    _(D,train,ctr,equals,-1)
    _(D,train,loss_dic,equals,{})
    _(D,val,equals,{})
    print('loading val_all_steer...')
    #_(D,val,all_data_moment_id_codes, equals, lo(opj(P[BAIR_CAR_DATA_PATH],'val_all_steer')))
    D[val][all_data_moment_id_codes] = lo(opj(P[BAIR_CAR_DATA_PATH],'val_all_steer'))
    _(D,val,ctr,equals,-1)
    _(D,val,loss_dic,equals,{})
    print('...done loading.')
    _(D,train,epoch_counter,equals,0)
    _(D,val,epoch_counter,equals,0)




    def _function_get_data(*args):
        Args = args_to_dictionary(args)
        True
        Data_moment = Segment_Data.get_data(
            Args[run_code],Args[seg_num],Args[offset],
            P[STRIDE]*P[N_STEPS],Args[offset]+0,P[N_FRAMES],ignore=P[IGNORE],
            require_one=P[REQUIRE_ONE],use_states=P[USE_STATES])
        return Data_moment


    def _function_next(*args):
        #print D[val][all_data_moment_id_codes][0]

        Args = args_to_dictionary(args)
        modev = Args[mode]

        #print D[val][all_data_moment_id_codes][0]
        if D[modev][ctr] >= len(da(D,modev,all_data_moment_id_codes)):
            D[modev][ctr] = -1
            D[modev][epoch_counter] += 1
        if D[modev][ctr] == -1:
            D[modev][ctr] = 0
            print('shuffle start')
            random.shuffle(D[modev][all_data_moment_id_codes])
            print('shuffle finished')
        #print D[val][all_data_moment_id_codes][0]
        data_moment_id_codev = D[modev][all_data_moment_id_codes][D[modev][ctr]]
        #data_moment_id_codev = da(D,modev,all_data_moment_id_codes)[D[modev][ctr]]
        #print D[val][all_data_moment_id_codes][0]
        D[modev][ctr] += 1
        #print D[val][all_data_moment_id_codes][0]
        D[val][all_data_moment_id_codes][0]
        #print D[val][all_data_moment_id_codes][0]
        return data_moment_id_codev

    _(D,get_data,equals,_function_get_data)
    _(D,next,equals,_function_next)
    return D
#EOF