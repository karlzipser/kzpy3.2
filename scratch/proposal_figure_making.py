h5p = opjD('Data/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py')
n = 'tegra-ubuntu_12Dec18_16h59m28s'
n = 'tegra-ubuntu_12Dec18_15h04m54s'
O=h5r(opj(h5p,n,'original_timestamp_data.h5py'))
images = O['image']['vals']
rindicies = rlen(images)
random.shuffle(rindicies)
for i in rlen(rindicies):
    j = rindicies[i]
    mi(images[j],img_title=d2s(j))
    spause()
    raw_enter()

#11858
#17476


images = lo('/home/karlzipser/Desktop/output_30steps.pkl')
#print len(images)
rindicies = range(11470)
random.shuffle(rindicies)
for i in rlen(rindicies):
    j = rindicies[i]
    mi(images[j],2,img_title=d2s(j))
    spause()
    raw_enter()



lst = [5725,8336,4587,553,10039,2993,7592,7960,9685,1304,9388,5632,8631,178,592,5253,609,8316,5275]
images = lo('/home/karlzipser/Desktop/output_1step.pkl')
for i in rlen(lst):
    j = lst[i]
    mi(images[j],3,img_title=d2s(j))
    spause()
    raw_enter()
