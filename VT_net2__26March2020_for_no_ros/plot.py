from kzpy3.vis3 import *


  
Colors = {'direct':'b','left':'r','right':'g'}
P = {}
P['behavioral_mode_list'] = ['left','direct','right']
lst=lo('/Users/karlzipser/Desktop/pts2D_multi_step.pkl')

figure('lst[-1]..');clf();plt_square();
a,b,c = 0,len(lst),1    
for i in range(a,b,c):
    if np.abs(lst[i]['steer'] - 49) < 100:
        for b in ['left','right','direct']:
            pts_plot(lst[i][b],color=Colors[b],sym=',') ###
        plot(lst[i]['x'],lst[i]['y'],'k.')
spause() ###



#,a
#time.sleep(60*30)
if 'lst' not in locals():
    Colors = {'direct':'b','left':'r','right':'g'}
    P = {}
    P['behavioral_mode_list'] = ['left','direct','right']
    lst=lo('/Users/karlzipser/Desktop/pts2D_multi_step.pkl')

Prediction2D_plot = CV2Plot(height_in_pixels=94,width_in_pixels=168,pixels_per_unit=7,y_origin_in_pixels=80)

Prediction2D_plot['verbose'] = False

indicies = []
images = []
freq = Timer(10)
for n in range(0,len(lst),1):
    indicies.append(lst[n]['index'])
    heading = -lst[n]['HEADING']
    #figure('lst[-1]..'); clf(); plt_square(); xysqlim(9)
    Prediction2D_plot['clear']()
    #a,b,c = 0,len(lst),10
    a,b,c = max(0,n-50), min(len(lst),n+250), 1
    for i in range(a,b,c):
        if np.abs(lst[i]['steer'] - 49) < 100:
            for b in ['left','right','direct']:
                pts = rotatePolygon(
                    lst[i][b]-na([[lst[n]['x'],lst[n]['y']]]),
                    heading
                )
                if i == n:
                    sym = '.'
                else:
                    sym = ','
                if False:
                    pts_plot(pts,color=Colors[b],sym=sym) ###
                Prediction2D_plot['pts_plot'](pts,Colors[b],add_mode=True)
    #mi(Prediction2D_plot['image'])
    #spause()
    
    img = Prediction2D_plot['show'](autocontrast2=True,scale=3.0,threshold=10,return_img=True)
    images.append(img)
    freq.freq()
    #raw_enter()

F = h5w(opjD('pts2D_multi_step.h5py'))
F.create_dataset('index',data=na(indicies))
F.create_dataset('images',data=na(images),dtype='uint8')          
F.close()

#,b
F = h5r(opjD('pts2D_multi_step.h5py'))
O = h5r(opjD('tegra-ubuntu_31Oct18_16h06m32s/original_timestamp_data.h5py'))
indicies = F['index'][:]
for i in rlen(indicies):
    mci(O['left_image']['vals'][indicies[i]],title='a',scale=3.)
    mci(F['images'][i],title='b',scale=3.,delay=1)


#EOF
