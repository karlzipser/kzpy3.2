
from kzpy3.vis3 import *
from kzpy3.drafts.randinfill import *

"""
python kzpy3/Data_app/lidar/second_steps_toward_depth_image.py --src /home/karlzipser/Desktop/runs_with_points__h5py --task raw
"""

plot_timer = Timer(0.1)

log_min,log_max = -0.25,1.5



def get_unprocessed_run(src):

    R = find_files_recursively(src,'original_timestamp_data.h5py',FILES_ONLY=True)
    run_folders = []
    for p in R['paths'].keys():
        run_folders.append(opj(src,p))

    temp = sggo(opjD('Depth_images/*'))

    runs_in_progress_or_done = []

    for t in temp:
        runs_in_progress_or_done.append(fname(t).split('.')[0])

    cg("runs_in_progress_or_done",runs_in_progress_or_done)

    run_folder = False

    for r in run_folders:
        if fname(r)[0]!= '_':
            if 'tegra-ubuntu_'  in r:

                if fname(r) not in runs_in_progress_or_done:
                    run_folder = r
            if run_folder:
                break

    return run_folder
    








def process_and_save_Depth_images(run_folder,time_limit=None):

    if type(time_limit) == int:
        time_limit_timer = Timer(time_limit)
    print run_folder
    spd2s("processing",fname(run_folder))

    the_run = fname(run_folder)

    os.system(d2s("touch",opjD('Depth_images',the_run)))

    if 'O' not in locals():
        cs('loading O')
        O = h5r(opj(run_folder,'original_timestamp_data.h5py' ))


    p = O['points']['vals']

    exception_timer = Timer(30)
    us=[]

    timer = Timer()

    Depth_images = {}
    Depth_images['run'] = the_run
    Depth_images['ts'] = []
    Depth_images['index'] = []
    Depth_images['depth'] = []
    Depth_images['intensity'] = []
    Depth_images['reflectivity'] = []
    Depth_images['display'] = []
    Depth_images['num_samples'] = []

    CA()

    range_n180_180 = range(-180,180)
    range_0_360 = range(0,360)
    range_n360_360 = range(-360,360)
    range_n90_90 = range(-90,90)
    range_n55_55 = range(-55,55)
    range_n60_60 = range(-60,60)

    zrange = range(-15,16,2)
    zranger = range(15,-16,-2)

    the_range = range_n180_180

    depth_img = zeros((32,len(the_range)))
    num_samples_img = zeros((32,len(the_range)))

    ctr1,ctr2=0,0
    the_encoder_index = 0
    the_encoder_ts = O['encoder']['ts'][the_encoder_index]
    while O['encoder']['vals'][the_encoder_index] < 0.75:
        the_encoder_ts = O['encoder']['ts'][the_encoder_index]
        the_encoder_index += 1
        cg("O['encoder']['vals'][the_encoder_index] =",O['encoder']['vals'][the_encoder_index], 'the_encoder_index =',the_encoder_index)#,'the_encoder_ts =',the_encoder_ts)
    


    for t in range(len(p)):

        if type(time_limit) == int:
            if time_limit_timer.check():
                cy("Reached time limit of",time_limit,"seconds, stopping with",the_run)
                break
        if True:#try:

            ts = O['points']['ts'][t]

            if ts < the_encoder_ts:
                continue

            mes = d2n("ts = ",ts," t = ",t,"/",len(p),", ",int(t/(1.0*len(p))*100),'%')

            cb(mes,sf=False)

            q = p[t,:,:].astype(np.float32)

            Data = {
                'depth':{},
                'intensity':{},
                'reflectivity':{},
            }

            for ky in Data.keys():
                for b in zrange:
                    Data[ky][b] = {}
                    for a in the_range:
                        Data[ky][b][a] = [0]

            for i in range(1024*16):

                x = q[i,0]
                y = q[i,1]
                z = q[i,2]
                intensity_maybe = q[i,4]
                reflectivity_maybe = q[i,5]

                a = np.degrees(angle_between((1,0), (x,y)) )

                if np.abs(a) <= 1.1*the_range[-1]:

                    b = np.degrees(angle_between((1,0), (np.sqrt(x**2+y**2),z)))

                    if y > 0:
                        a*=-1

                    if z < 0:
                        b *= -1
                    try:
                        ctr2+=1
                        ai = int(a)
                        bi = b +0.5
                        if bi < -15:
                            bi = -15
                        elif bi < -13:
                            bi = -13
                        elif bi < -11:
                            bi = -11
                        elif bi < -9:
                            bi = -9
                        elif bi < -7:
                            bi = -7
                        elif bi < -5:
                            bi = -5
                        elif bi < -3:
                            bi = -3
                        elif bi < -1:
                            bi = -1
                        elif bi < 1:
                            bi = 1
                        elif bi < 3:
                            bi = 3
                        elif bi < 5:
                            bi = 5
                        elif bi < 7:
                            bi = 7
                        elif bi < 9:
                            bi = 9
                        elif bi < 11:
                            bi = 11
                        elif bi < 13:
                            bi = 13
                        else:
                            bi = 15

                        dist = np.sqrt( x**2 + y**2 + z**2 )

                        Data['depth'][bi][ai].append(dist)
                        Data['intensity'][bi][ai].append(intensity_maybe)
                        Data['reflectivity'][bi][ai].append(reflectivity_maybe)

                    except Exception as e:
                        ctr1+=1
                        if exception_timer.check():
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            cs(exc_type,file_name,exc_tb.tb_lineno,'exceptions are ',dp(100*ctr1/(1.0*ctr2)),"% of computations")
                            exception_timer.reset()

            for ky in Data.keys():
                depth_img *= 0
                ctr_10 = 0
                for b in zranger:
                    m = []
                    ns = []
                    ctr_11 = 0
                    for ai in sorted(Data[ky][b]):

                        num_samples = len(Data[ky][b][ai]) - 1
                        ns.append(num_samples)
                        if num_samples > 0:
                            m.append(np.mean(Data[ky][b][ai][1:]))
                        else:
                            m.append(0)
                        ctr_11 += 1
                    for dd in range(2):
                        depth_img[ctr_10,:] = m
                        num_samples_img[ctr_10,:] = ns
                        ctr_10 += 1
                if ky == 'depth':
                    Depth_images['num_samples'].append(num_samples_img.copy())
                Depth_images[ky].append(depth_img.copy())

            Depth_images['ts'].append(ts)
            Depth_images['index'].append(t)
            
            randinfill(
                [Depth_images['depth'][-1],
                Depth_images['intensity'][-1],
                Depth_images['reflectivity'][-1]],
                Depth_images['num_samples'][-1]
            )
            print type(Depth_images['depth']),shape(Depth_images['depth']),shape(Depth_images['depth'][-1])

            if True:#plot_timer.check():

                for ky in ['num_samples','depth','intensity','reflectivity']:
                    mci(
                        z55(Depth_images[ky][-1]),
                        scale=3.0,
                        color_mode=cv2.COLOR_GRAY2BGR,
                        title=d2n(the_run.replace('tegra-ubuntu_',''),': ',ky)
                    )

        """
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
        """

    O.close()

    try:
        os.system(d2s("rm",opjD('Depth_images',the_run)))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        
    save_Depth_images(Depth_images,the_run)





def show_depth_imgs(Depth_images,start=0,stop=-1):

    if type(Depth_images['run']) == str:
        the_run = Depth_images['run']
    else:
        the_run = Depth_images['run'][0] # because of hdf5 strings

    for img,index in zip(Depth_images['depth'][start:stop],Depth_images['index'][start:stop]):
        figure(d2s(the_run,'show_depth_imgs'),figsize=(2,1))
        mi(img,d2s(the_run,'show_depth_imgs'));

        spause()






def save_Depth_images(Depth_images,the_run,path=opjD('Depth_images')):
    D = Depth_images
    file_path = opj(path,d2p(the_run,'Depth_image','h5py'))
    F = h5w(file_path)
    pd2s('saving',the_run,'Depth_images...')
    for topic_ in Depth_images.keys():
        pd2s('\t',topic_,len(D[topic_]),type(D[topic_]),shape(D[topic_]))

        if type(D[topic_]) == str:
            try:
                s = F.create_dataset(topic_,(1,),dtype=h5py.special_dtype(vlen=str))
                s[:] = the_run
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)            
        else:
            F.create_dataset(topic_,data=D[topic_])     
    F.close()
    pd2s('...saving complete.')












def make_log_versions_of_images(depth_images_path):

    """
    python kzpy3/Data_app/lidar/first_steps_toward_depth_image4.py task log path ~/Desktop/Depth_images_continue/
    """

    depth_image_files = sggo(depth_images_path,'*.Depth_image.h5py')

    for depth_image_file in depth_image_files:

        error_file = depth_image_file+'.error'
        touched_file = depth_image_file+'.work_in_progress'
        if len(sggo(touched_file)) > 0:
            continue
        if len(sggo(error_file)) > 0:
            continue
            
        os.system(d2s('touch',touched_file))


        try:
            D = h5rw(depth_image_file)
            r = D['real'][:]
            pa = Progress_animator(len(r),message='r')

            display = False


            shape_r = shape(r[0])
            height,width = shape_r[0],shape_r[1]

            g = zeros((33,360))
            z = zeros((32,360))
            e = r[0,:,:]

            processed_depth_images = []

            display_timer = Timer(2)

            clear_screen()
            cs("Processing",depth_image_file)
            for i in rlen(r):

                pa['update'](i)

                if i > 0:
                    a=r[i,:,:]
                    b = a==0.0
                    c = b.astype(int)
                    d = (1-c)*a + c*e
                    e = d.copy()
                    f = np.log10(d+.001)
                    h = (f>log_max).astype(int)
                    k = (1-h)*f + h*(z+log_max)
                    h = (f<log_min).astype(int)
                    k = (1-h)*k + h*(z+log_min)
                    if i == 1:
                        processed_depth_images.append(k)
                        # since first image has no previous, make first image equal second
                    processed_depth_images.append(k)
                    if display_timer.check():
                        g[:32,:] = k
                        g[32,0] = 1.5
                        g[32,1:] = -0.25
                        mi(g,'log10 depth image')
                        if False:
                            figure('hist');clf()
                            hist(d.flatten(),bins=100);xylim(0,100,0,200)
                            figure('log10 hist');clf()
                            hist(k.flatten(),bins=100);xylim(-2,2,0,200)
                        display_timer.reset()
                spause()
            assert len(processed_depth_images) == len(D['index'][:])
            D.create_dataset('log',data=na(processed_depth_images))
            D.close()
            os.system('rm '+touched_file)
            os.system(d2s('mv',depth_image_file,depth_image_file.replace('.Depth_image.h5py','.Depth_image.log.h5py')))
            
        except Exception as e:
            os.system('rm '+touched_file)
            os.system('touch '+error_file)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)










def make_resize_and_flip_versions_of_images(depth_images_path):

# PUT IN ZERO TO ONE SCALING

    depth_image_files = sggo(depth_images_path,'*.Depth_image.log.h5py')
    
    img_bigger = zeros((95,168))

    for depth_image_file in depth_image_files:

        error_file = depth_image_file+'.error'
        touched_file = depth_image_file+'.resize_flip_work_in_progress'
        if len(sggo(touched_file)) > 0:
            continue
        if len(sggo(error_file)) > 0:
            continue
            
        os.system(d2s('touch',touched_file))


        try:
            D = h5rw(depth_image_file)
            r = D['log'][:]
            
            pa = Progress_animator(len(r),message='r')

            resized = []
            resized_flipped = []

            display_timer = Timer(2)

            
            cs("\n\nProcessing",depth_image_file,"for resize and flip.")

            for i in rlen(r):
                pa['update'](i)
                #print shape(r[i,:,:])
                img = cv2.resize(r[i,:,62:298],(168,94))
                #print shape(img_bigger)
                #print shape(img)
                img_bigger = img_bigger * 0
                img_bigger[:94,:] = img
                img_bigger[94,0] = log_min
                img_bigger[94,1] = log_max
                
                img = 255*z2o(img_bigger)[:94,:] # the 255 multiple is to put these images into same range as the rgb images
                assert shape(img) == (94,168)
                resized.append(img)
                resized_flipped.append(cv2.flip(img,1))
                if display_timer.check():
                    mi(img_bigger,'img_bigger')
                    mi(r[i,:,:],'log depth image')
                    mi(resized[-1],'log resize depth image')
                    display_timer.reset()
                spause()
            assert len(resized) == len(D['index'][:])
            assert len(resized_flipped) == len(D['index'][:])
            D.create_dataset('resized',data=na(resized))
            D.create_dataset('resized_flipped',data=na(resized_flipped))
            D.close()
            os.system('rm '+touched_file)
            os.system(d2s('mv',depth_image_file,depth_image_file.replace('.Depth_image.log.h5py','.Depth_image.log.resize.flip.h5py')))
            
        except Exception as e:
            D.close()
            os.system('rm '+touched_file)
            os.system('touch '+error_file)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            break





def asign_left_timestamps(depth_images_path,runs_location):

    import kzpy3.Data_app.classify_data as classify_data
    P = {}
    P['experiments_folders'] = []
    classify_data.find_locations( runs_location,P['experiments_folders'] )# (opjm("1_TB_Samsung_n1"),P['experiments_folders'])
    P['experiments_folders'] = list(set(P['experiments_folders']))

    P['run_name_to_run_path'] = {}

    for experiments_folder in P['experiments_folders']:
        if fname(experiments_folder)[0] == '_':
            continue
        print experiments_folder
        locations = sggo(experiments_folder,'*')
        for location in locations:
            if fname(location)[0] == '_':
                spd2s('ignoring',location)
                continue
            print location
            b_modes = sggo(location,'*')
            print b_modes
            for e in b_modes:
                if fname(e)[0] == '_':
                    continue
                if fname(e) == 'racing':
                    continue
                spd2s(fname(e))
                for r in sggo(e,'h5py','*'):
                    run_name = fname(r)
                    P['run_name_to_run_path'][run_name] = r
                    cg(sggo(r,'left_timestamp_metadata_right_ts.h5py'))


    depth_image_files = sggo(depth_images_path,'*.Depth_image.log.resize.flip.h5py')

    for depth_image_file in depth_image_files:
        run_name = fname(depth_image_file).split('.')[0]
        cb("<run_name =",run_name,"> depth_image_file = <",depth_image_file,">")
        assert run_name in P['run_name_to_run_path']
        

        error_file = depth_image_file+'.error'
        touched_file = depth_image_file+'.work_in_progress'
        if len(sggo(touched_file)) > 0:
            continue
        if len(sggo(error_file)) > 0:
            continue
            
        os.system(d2s('touch',touched_file))


        try:
            D = h5rw(depth_image_file)
            index = D['index'][:]
            lidar_ts = D['ts'][:]
            L = h5r(opj(P['run_name_to_run_path'][run_name],'left_timestamp_metadata_right_ts.h5py'))
            left_camera_ts = L['ts'][:]
            L.close()

            

            display_timer = Timer(2)

            cs("\n\nProcessing",depth_image_file,"for left timestamps.")

            lidar_index = 0

            D_left_to_lidar_index = 0 * left_camera_ts

            len_left_ts = len(left_camera_ts)

            pa = Progress_animator(len_left_ts,message='r')

            finished = False

            for i in range(len_left_ts):
                if finished:
                    break


                pa['update'](i)

                left_ts = left_camera_ts[i]

                while lidar_ts[lidar_index] < left_ts:

                    if lidar_index >= len(lidar_ts)-1:
                        finished = True
                    if finished:
                        break

                    lidar_index += 1
                    pa = Progress_animator(len(index),message=d2s(left_ts))

                cg(dp(lidar_ts[lidar_index]-left_ts,3),lidar_index,i)

                D_left_to_lidar_index[i] = lidar_index


            D.create_dataset('left_to_lidar_index',data=D_left_to_lidar_index)
            D.close()
            os.system('rm '+touched_file)
            os.system(d2s('mv',depth_image_file,depth_image_file.replace('.Depth_image.log.resize.flip.h5py','.Depth_image.log.resize.flip.with_left_ts.h5py')))
            
        except Exception as e:
            D.close()
            os.system('rm '+touched_file)
            os.system('touch '+error_file)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
    




if False:

    def transfer_lacking(src,dst):
        src_files = sggo(src,'*.h5py')
        src_runs = []
        for s in src_files:
            src_runs.append(fname(s).split('.')[0])
        existing_files = sggo(dst,'*.h5py')
        existing_runs = []
        for e in existing_files:
            existing_runs.append(fname(e).split('.')[0])

        dont_copy = []
        for s in src_runs:
            for e in existing_runs:
                if s == e:
                    cr(s,"==",e)
                    dont_copy.append(s)
            #cg("cp",s,"to",dst)
        for s in src_runs:
            if s not in dont_copy:
                cg("copy",s)
                os.system(d2s("cp",opj(src,s+"*"),dst))


    
    src = opjD('Depth_images.log')
    dst = opjD('Depth_images.log.resize.flip')
    transfer_lacking(src,dst)


if __name__ == '__main__':

    ############################
    #

    Arguments['path'] = opjD('Depth_images')
    if 'limit' not in Arguments:
        Arguments['limit'] = None
    if 'src' in Arguments:
        Arguments['runs_location'] = Arguments['src']


    if Arguments['task'] in ['raw','all']:
        run_folder = get_unprocessed_run(Arguments['src'])
        if run_folder:
            process_and_save_Depth_images(run_folder,Arguments['limit'])
        else:
            cr("no runs left to process")

    
    if Arguments['task'] in ['log','all']:
        depth_images_path = Arguments['path']
        make_log_versions_of_images(depth_images_path)


    if Arguments['task']  in ['resize_flip','all']:
        depth_images_path = Arguments['path']
        make_resize_and_flip_versions_of_images(depth_images_path)


    if Arguments['task'] in ['left_ts','all']:
        depth_images_path = Arguments['path']
        runs_location = Arguments['runs_location']
        asign_left_timestamps(depth_images_path,runs_location)
    
    #
    ############################
    


#EOF







