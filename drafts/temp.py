if 'D' not in locals():
    D = h5r(opjD('Data/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_14h29m28s/original_timestamp_data.h5py'))

i = D['image']['vals'] 

if False:
    new_img = zeros((690,64,3),np.uint8)

    for j in range(10000,20000,10):

        img = 0 * i[j,:,:,:]

        mi(i[j,:,:,:],'i')

        #mi(i[j,:,:,0],0)

        #mi(i[j,:,:,1],1)

        #mi(i[j,:,:,2],2)

        a = i[j,:,:,2]
        a[a>255] = 255#a[a>30] = 30
        img[:,:,0] =  255 - a


        a = 1700.*i[j,:,:,1]/300.
        a[a>255] = 255
        img[:,:,1] = a #*1700./300.


        img[:,:,2] =  255-i[j,:,:,0]#/4500.*300

        new_img = cv2.resize(img,(690,64),interpolation=0)
        mi(new_img,'new_img')

        spause()
        raw_enter()



def image_to_rgb_v1(img_in):
    img = 0 * img_in
    a = img_in[:,:,2]
    a[a>255] = 255
    img[:,:,0] =  255 - a

    a = 1700.*img_in[:,:,1]/300.
    a[a>255] = 255
    img[:,:,1] = a

    img[:,:,2] =  255-img_in[:,:,0]

    new_img = cv2.resize(img,(690,64),interpolation=0)

    return new_img



for j in range(10000,20000,10):

    new_img = image_to_rgb_v1(i[j,:,:,:])

    mi(new_img,'new_img')

    spause()
    raw_enter()



# 0 == other
# 1 == camera
# 2 == depth

if False:
    a = D['depth'][i,:,:]/2.0*255
    a[a>255] = 255
    a[a<0] = 0
    image[:,:,0] = 255-a

    a = D['camera'][i,:,:]
    if False:
        b = a.flatten()
        hist(b);spause()
    a = a/300.0*255
    a[a>255] = 255
    a[a<0] = 0
    image[:,:,1] = a

    a = D['other'][i,:,:]
    a = a/100.0*255
    a[a>255] = 255
    a[a<0] = 0
    a = 255-a

    """ # code from os1_ros.cpp to adjust data for image
    if (point.reflectivity<500){ref255=500;}
    else if (point.reflectivity>5000){ref255=5000;}
    ref255=(int)(255*(ref255-500)/4500.0);
    if (ref255<0) std::cout << "error1";
    if (ref255>255) std::cout << "error2";

    if (point.intensity>1700) int255=255;
    else int255 = (int)(255*(point.intensity/1700));
    if (int255<0) std::cout << "error3";
    if (int255>255) std::cout << "error4";

    const float rmax = 5.0;
    if (r>rmax){r255=255;}
    else {r255=(int)(r/rmax*255);}
     if (r255<0) std::cout << "error5";
    if (r255>255) std::cout << "error6";
    """




def measure_steps(ts):
    steps = []
    for i in range(1,len(ts)):
        steps.append(ts[i]-ts[i-1])
    return steps




runs = []
A = find_files_recursively(opjD('h5py_data_reprocessed_from_other_drives'),'tegra*')
#A = find_files_recursively(opjD('h5py_have_already'),'tegra*')
for b in A['paths'].keys():
    runs += A['paths'][b]
runs

new_runs = runs

runs = []
A = find_files_recursively(opjD('Data'),'tegra*')
for b in A['paths'].keys():
    runs += A['paths'][b]

old_runs = runs


for n in new_runs:
    if n in old_runs:
        print n,True
    else:
        print n,False







top = opjD('Data')
A = find_files_recursively(top,'tegra-ubuntu_*',DIRS_ONLY=True)

P = A['paths']
Tasks = {'left_right_center':[],'left_direct_stop':[]}
q = []
for a in P.keys():
    for b in P[a]:
        original_path = opj(top,a,b,'original_timestamp_data.h5py')
        D = h5r(original_path)
        for t in Tasks.keys():
            if t in a:
                Tasks[t].append(D['left_image']['ts'][0])
        D.close()
CA()
plot(sorted(Tasks['left_right_center']),'.')
plot(sorted(Tasks['left_direct_stop']),'.')




