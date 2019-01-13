from __future__ import division
from kzpy3.vis3 import *
assert(1/2 == 0.5)
import kzpy3.scratch.image as image

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L,O,___ = open_run("Mr_Black_25Jul18_14h44m55s_local_lrc",
                opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py"),want_list=['L','O'])

topics = [
    #u'acc_x',
    #u'acc_x_meo',
    #u'acc_y',
    #u'acc_y_meo',
    #u'acc_z',
    #u'acc_z_meo',
    #u'behavioral_mode',
    #u'button_number',
    #u'cmd_motor',
    #u'cmd_steer',
    #u'drive_mode',
    #u'encoder',
    #u'encoder_meo',
    u'gyro_heading_x',
    #u'gyro_heading_x_meo',
    #u'gyro_heading_y',
    #u'gyro_heading_y_meo',
    #u'gyro_heading_z',
    #u'gyro_heading_z_meo',
    #u'gyro_x',
    #u'gyro_x_meo',
    #u'gyro_y',
    #u'gyro_y_meo',
    #u'gyro_z',
    #u'gyro_z_meo',
    #u'human_agent',
    #u'left_ts_deltas',
    #u'motor',
    #u'place_choice',
    #u'right_ts',
    #u'steer',
    #u'ts',
]

max_steps = 500
P = {}

P['index'] = 5

for t in topics:
    P[opj(t,'index')] = 0
    P[opj(t,'data')] = None#zeros((1,2))
    P[opj(t,'min')] = -0.1#2**16
    P[opj(t,'max')] = 0.1#-2**16

window_seconds_width = 5

cat = zeros((1,2))
def update(P):

    P['ts'] = L['ts'][P['index']]
    for t in topics: 

        while O[t]['ts'][P[opj(t,'index')]] < P['ts']:
            #print t,P[opj(t,'index')]
            value = O[t]['vals'][P[opj(t,'index')]]
            
            if value > P[opj(t,'max')]:
                P[opj(t,'max')] = value

            if value < P[opj(t,'min')]:
                P[opj(t,'min')] = value

            cat[0,0] = O[t]['ts'][P[opj(t,'index')]]
            cat[0,1] = value
            if P[opj(t,'data')] == None:
                P[opj(t,'data')] = cat
            else:
                P[opj(t,'data')] = np.concatenate((P[opj(t,'data')],cat),0)
            P[opj(t,'index')] += 1

        MN,MX = P[opj(t,'min')],P[opj(t,'max')]
        s = 0.9999
        MX = s*MX + (1-s)*(MX-MN)/2.0
        MN = s*MN + (1-s)*(MX-MN)/2.0
        P[opj(t,'min')],P[opj(t,'max')] = MN,MX            
        if True:
            for i in rlen(P[opj(t,'data')]):
                if P[opj(t,'data')][i,0] >= P['ts'] - window_seconds_width:
                    break
            P[opj(t,'data')] = P[opj(t,'data')][i:]
        else:
            if len(P[opj(t,'data')]) > max_steps:
                P[opj(t,'data')] = P[opj(t,'data')][-max_steps:,:]
    P['index'] += 1
    Hz.freq()

img = image.get_blank_image(400,500) #########

plot_timer = Tr(2/30)
message = Tr(3)
tr = Tr(500)
Hz=Tr(3)


while not tr.c():
    
    if True:#:try:
        for i in range(1):
            update(P)
        plot_timer.reset()
        ctr = 0
        image.place_image_in_image2(img,O['left_image']['vals'][P['index']],row=(2,3),col=(2,3)) #########
        image.place_image_in_image2(img,O['right_image']['vals'][P['index']],row=(2,3),col=(3,3)) #########

        for t in topics:

            ylm = (0.8*P[opj(t,'min')],0.8*P[opj(t,'max')])

            cs = na((255,255,255))
            if '_x' in t:
                cs = na((255,0,0))
            if 'heading' in t:
                cs = na((255,255,255))
            if '_y' in t:
                cs = na((0,255,0))
                
            if '_z' in t:
                cs = na((0,0,255))
            if 'button_number' in t:
                cs = na((255,255,0))
                ylm = (0,4)                
            if 'motor' in t:
                cs = na((0,0,255))
                ylm = (0,99)
            if 'steer' in t:
                cs = na((255,0,0))
                ylm = (0,99)
            if 'encoder' in t:
                cs = na((0,255,255))

            
            ctr += 1

            r = len(topics)-ctr+1
            xys = image.get_float_pixels( #########
                xys=na(P[opj(t,'data')]),
                img_shape=shape(img),
                col=(1.1,2),
                row=(r+0.5,1+len(topics)),
                box=((P['ts'] - window_seconds_width,P['ts']),ylm)
            )
            image.img_pts_plot(img,xys,cs) #########
        
        mci(img)
        img *= 0

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            





#EOF
