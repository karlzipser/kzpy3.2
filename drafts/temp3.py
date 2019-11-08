





#################
roscore &


python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 0 --step 0 --initial_index 25000

rosplay_menu.py


#python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019__/nodes --dic P
python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019_rgb_v1/nodes --dic P
# 8,12,-1,8,10

#python kzpy3/Cars/j26June2019__/nodes/network_node.py desktop_mode 1
python kzpy3/Cars/j26June2019_rgb_v1/nodes/network_node.py desktop_mode 1

python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py

python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__5April2019_2__18April2019_for_speed --dic P





L = h5r('/home/karlzipser/Desktop/Data/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_14h29m28s/left_timestamp_metadata_right_ts.h5py')

e = L['encoder']
m = L['motor']
a = L['acc_x_meo']
clf()
plot(m,e,'.')




#,a

network_to_validate = 'Sq120_ldr_output_4April2019'

weights_path = opjD('Networks',network_to_validate,'weights')

ctime_sorted_weightfiles = sort_dir_by_ctime(weights_path)

selected_weightfiles = []
num = 10
for i in range(0,len(ctime_sorted_weightfiles),len(ctime_sorted_weightfiles)/num):
    selected_weightfiles.append(ctime_sorted_weightfiles[i])
if ctime_sorted_weightfiles[-1] not in selected_weightfiles:
    selected_weightfiles.append(ctime_sorted_weightfiles[-1])
so(opjD('Networks',network_to_validate,'Val_lists'),
    {'ctime_sorted_weightfiles':ctime_sorted_weightfiles,
    'selected_weightfiles':selected_weightfiles})
for w in selected_weightfiles:
    sys_str =  d2s(
        "python kzpy3/Train_app/Sq120_ldr_output_4April2019/Main.py",
        "--VALIDATION_WEIGHTS_FILE_PATH",
        w
    )
    print sys_str
    os.system(sys_str)





Val_lists = lo(opjD('Networks',network_to_validate,'Val_lists'))
ctime_sorted_weightfiles = Val_lists['ctime_sorted_weightfiles']
selected_weightfiles = Val_lists['selected_weightfiles']
validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))
validation_losses = []
for s in selected_weightfiles:
    for v in validation_loss_files:
        if fname(s) in v:
            o = lo(v)
            validation_losses.append(np.median(na(o)))
            break
clf()
plot(validation_losses,'k.-')
plt.title(d2s('validation of',network_to_validate))
plt.ylabel('loss')
plt.xlabel('weightfiles')


#,b

V = {}
ctr = 0
validation_loss_files = sggo(opjD('Networks',network_to_validate,'validation_loss','*'))

for s in selected_weightfiles:
    V[fname(s)] = {'ctr':ctr,'lst':[]}
    ctr += 1

for s in selected_weightfiles:
    for v in validation_loss_files:
        print s,v
        if fname(s) in v:
            o = lo(v)
            V[fname(s)]['lst'] += o

validation_losses = range(len(selected_weightfiles))
for a in V.keys():
    validation_losses[V[a]['ctr']] = np.median(na(V[a]['lst']))

clf()
plot(validation_losses,'k.-')
plt.title(d2s('validation of',network_to_validate))
plt.ylabel('loss')
plt.xlabel('weightfiles')




#EOF
