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


def pt_in_2D_to_image(x,y):
    b = fit3d.Point3(x,0,y)
    c = fit3d.project(b, fit3d.mat)
    return c.x,c.y


m = 0.47885706 # from Mr. Blue
b = -21.76993126

backup_parameter = 1.0

for j in range(100):

    i = np.random.randint(5000,len(I['L']))
    mi(I['R'][i],'R')
    mi(I['L'][i],'L')
    for x_ in arange(-0.5,0.51,0.25):
        for y_ in arange(0.,3.1,0.25):
            x,y = pt_in_2D_to_image(x_,y_-backup_parameter)
            for s in ['L','R']:
                fig = figure(s)
                if s == 'L':
                    xy_list = [[x,y]]
                else:
                    dx = max(0,y*m+b)
                    xy_list = [[x-dx,y]]
                x = xy_list[0][0]
                y = xy_list[0][1]
                good = True
                if x < 0 or x >= 168:
                    good = False
                elif y < 0 or y >= 94:
                    good = False
                if good:
                    plot(x,y,'r.')

                if s == 'R':
                    cg(dx)
    spause()
    raw_enter()

#if __name__ == '__main__':
 
#EOF


