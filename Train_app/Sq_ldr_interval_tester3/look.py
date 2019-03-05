from kzpy3.vis3 import *
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)

locations = []
Runs = {}
find_locations(opjD('Data'),locations,False)
run_paths(locations,Runs)

if True:
    #rn = 'tegra-ubuntu_15Nov18_20h52m45s'
    rn = 'tegra-ubuntu_15Nov18_20h53m56s'

    files = sggo(opjD('tegra-ubuntu_15Nov18_20h53m56s__interval_tests__ref_index_48605',rn+'__interval_tests__ref_index_*.pkl'))
    np.random.shuffle(files)
    min_index = 0#5500
    cr('min_index =',min_index)

    seen = [];replies = []
    if 'seen' not in locals():
        seen = []
    if 'replies' not in locals():
        replies = []
    for f in files:
        cy(f)
        #run_name = fname(f).split('__interval')[0]
        run_name = fname(f).split('__')[-1].replace('.pkl','')
        O_path = opjD(Runs[run_name],'original_timestamp_data.h5py')

        O = h5r(O_path)
        imgs = O['left_image']['vals']

        #cg(replies)
        #cb(seen)
        if f in seen:
            continue
        seen.append(f)
        i = 0
        try:
            cm(0)
            all_values = lo(f)['LDR values']
            values = []
            #cr(len(all_values),len(imgs),ra=0)
            while i < len(all_values):
                indx = i
                #print i,len(all_values)
                max_val = all_values[i]
                for j in range(30*90):
                    if i+j >= len(all_values):
                        break
                    if all_values[i+j] < max_val:
                        indx = i+j
                        max_val = all_values[i+j]
                i += j
                values.append((indx,max_val,run_name))
            s = []
            indicies = []
            threshold = 0.0
            ctr = 0
            while (ctr < 49 and threshold < 0.25) or (ctr < 9 and threshold < 0.25):
                ctr = 0
                threshold += 0.01
                for i in rlen(values):
                    val = values[i][1]
                    if val < threshold:
                        ctr += 1
            cm(1)
            for i in rlen(values):
                idx = values[i][0]
                val = values[i][1]
                if val < threshold:
                    if idx > min_index:
                        indicies.append(idx)
                        s.append(imgs[idx,:,:,:])
                        #print i
                        #clf();mi(imgs[i,:,:,:],2);pause(0.1)
            cm(2)
            print ctr,threshold,len(values)
            s = na(s)
            v = vis_square2(z55(s),10)
            mi(v);spause()
            replies.append((f,raw_enter(fname(f))))
            O.close()
            cm(3)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)



if False:
    #rn = 'tegra-ubuntu_15Nov18_20h52m45s'
    rn = 'tegra-ubuntu_15Nov18_20h53m56s'
    O_path = opjD('Data/2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py/'+rn+'/original_timestamp_data.h5py')
    O = h5r(O_path)
    imgs = O['left_image']['vals']
    files = sggo(opjD(rn,rn+'*'))
    np.random.shuffle(files)
    min_index = 0#5500
    cr('min_index =',min_index)
    seen = [];replies = []
    if 'seen' not in locals():
        seen = []
    if 'replies' not in locals():
        replies = []
    for f in files:
        cg(replies)
        cb(seen)
        if f in seen:
            continue
        seen.append(f)
        i = 0
        try:
            all_values = lo(f)['LDR values']
            values = []

            while i < len(all_values):
                indx = i
                #print i,len(all_values)
                max_val = all_values[i]
                for j in range(300):
                    if i+j >= len(all_values):
                        break
                    if all_values[i+j] < max_val:
                        indx = i+j
                        max_val = all_values[i+j]
                i += j
                values.append((indx,max_val))
            s = []
            indicies = []
            threshold = 0.0
            ctr = 0
            while (ctr < 49 and threshold < 0.20) or (ctr < 9 and threshold < 0.25):
                ctr = 0
                threshold += 0.01
                for i in rlen(values):
                    val = values[i][1]
                    if val < threshold:
                        ctr += 1

            for i in rlen(values):
                idx = values[i][0]
                val = values[i][1]
                if val < threshold:
                    if idx > min_index:
                        indicies.append(idx)
                        s.append(imgs[idx,:,:,:])
                        #print i
                        #clf();mi(imgs[i,:,:,:],2);pause(0.1)
            print ctr,threshold,len(values)
            s = na(s)
            v = vis_square2(z55(s),10)
            mi(v);spause()
            replies.append((f,raw_enter(fname(f))))

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

#EOF