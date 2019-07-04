from kzpy3.vis3 import *
import kzpy3.misc.fit3d as fit3d

if 'O' not in locals():
    if using_osx():
        O=h5r('/Users/karlzipser/Desktop_19Feb19_08h49m53s/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_24Jul18_20h04m17s_local_lrc/original_timestamp_data.h5py')
    else:
        O = h5r('/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/tu_8to12Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_08Oct18_19h15m15s/original_timestamp_data.h5py')
    I = {}
    I['L'] = O['left_image']['vals']
    I['R'] = O['right_image']['vals']


backup_parameter = 1.0

figure(1)
clf()
mi(I['L'][10000])
#plt_square()#xylim(0,168,0,94)

for x in arange(-0.5,0.505,0.1):
    for yy in arange(0.,3.05,0.1):
        y = yy
        #x = np.random.random()*1.-0.5
        #y = np.random.random()*10.-1


        b = fit3d.Point3(x,0,y)

        c = fit3d.project(b, fit3d.mat)
        print c.x,c.y
        good = True

        if c.x < 0 or c.x >= 168:
            good = False
        elif c.y < 0 or c.y >= 94:
            good = False

        if good:
            plot(c.x,c.y,'r.')
            spause()
            time.sleep(0.001)
raw_enter()
