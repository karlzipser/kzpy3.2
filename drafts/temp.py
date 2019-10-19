D = h5r(opjD('Data/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_14h29m28s/original_timestamp_data.h5py'))

i = D['image']['vals'] 


for j in range(10000,20000,10):
    mi(i[j,:,:,:])

    mi(i[j,:,:,0],0)

    mi(i[j,:,:,1],1)

    mi(i[j,:,:,2],2)

    spause()
    raw_enter()


# 0 == other
# 1 == camera
# 2 == depth




