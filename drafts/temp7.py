

from kzpy3.vis3 import *


setup_Default_Arguments(
    {
        'a':1,
        'b':2,
    }
)

kprint(Arguments)


files = sggo(opjD('Interval_data/*.pkl'))



#,a
Runs = {}
for x in rlen(files):
    kprint(x,title='file number')
    I = lo(files[x])
    for n in I.keys():
        for i in I[n]:
            #f0 = i[0][0]
            #f1 = i[1][0]
            for j in [0,1]:
                f = i[j][0]
                if f not in Runs:
                    H = find_files_recursively(opjD('Data'),f,DIRS_ONLY=True)
                    Runs[f] = H['paths'].keys()[0]

Os = {}
for r in Runs.keys():
    p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
    Os[r] = h5r(p)





mi(Os['tegra-ubuntu_31Oct18_16h06m32s']['left_image']['vals'][50000])

img = zeros((94,168*2,3),np.uint8)

img[:,:168,:] = Os['tegra-ubuntu_31Oct18_16h06m32s']['left_image']['vals'][50000]
img[:,168:,:] = Os['tegra-ubuntu_31Oct18_16h06m32s']['left_image']['vals'][50010]
mi(img,img_title=d2s(0.9))
#,b
#EOF
