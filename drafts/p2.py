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

figure(1)
clf()
mi(I['L'][10000])
#plt_square()#xylim(0,168,0,94)

if False:
    for x_ in arange(-0.5,0.505,0.2):
        for y_ in arange(0.,3.05,0.2):

            x,y = pt_in_2D_to_image(x_,y_-backup_parameter)

            good = True
            if x < 0 or x >= 168:
                good = False
            elif y < 0 or y >= 94:
                good = False
            if good:
                plot(x,y,'r.')
                spause()
                time.sleep(0.001)


if True:
    XYs = {}
    XYs['L'] = []
    XYs['R'] = []
    #CA()
    #for j in range(100):
    i = np.random.randint(5000,len(I['L']))
    mi(I['R'][i],'R')
    mi(I['L'][i],'L')
    for x_ in arange(-0.5,0.51,0.25):
        for y_ in arange(0.,3.1,0.25):

            x,y = pt_in_2D_to_image(x_,y_-backup_parameter)
            """
            good = True
            if x < 0 or x >= 168:
                good = False
            elif y < 0 or y >= 94:
                good = False
            if good:
                plot(x,y,'r.')
                spause()
                time.sleep(0.001)
            """
            for s in ['L','R']:
                fig = figure(s)
                #clf()
                
                #Cdat = Click_Data(FIG=fig)
                if s == 'L':
                    xy_list = [[x,y]]#Cdat['CLICK'](NUM_PTS=1)
                else:
                    #xy_list = [[x,y]]
                    #x = xy_list[0][0]
                    #y = xy_list[0][1]
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
                #pts_plot(na(xy_list),'r')
                
                #XYs[s] += xy_list
                if s == 'R':
                    cg(dx)
                    #raw_enter()
spause()
spause()

#raw_enter()

if False:
    XYs = {}
    XYs['L'] = []
    XYs['R'] = []
    CA()
    for j in range(100):
        i = np.random.randint(5000,len(I['L']))

        for s in ['L','R']:
            fig = figure(s)
            clf()
            mi(I[s][i],s)
            Cdat = Click_Data(FIG=fig)
            if s == 'L':
                xy_list = Cdat['CLICK'](NUM_PTS=1)
            else:
                x = xy_list[0][0]
                y = xy_list[0][1]
                dx = max(0,y*m+b)
                xy_list = [[x-dx,y]]
            pts_plot(na(xy_list),'r')
            spause()
            XYs[s] += xy_list
            if s == 'R':
                cg(dx)
                raw_enter()
