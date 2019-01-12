from __future__ import division
from kzpy3.vis3 import *
assert(1/2 == 0.5)
import kzpy3.scratch.image as image

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L = h5r(opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py",
        "Mr_Black_25Jul18_14h44m55s_local_lrc/left_timestamp_metadata_right_ts.h5py"))

topics = [
    u'acc_x',
    

    #u'acc_x_meo',
    u'acc_y',

    #u'acc_y_meo',
    u'acc_z',
    

    #u'acc_z_meo',
    #u'behavioral_mode',
    u'button_number',
    #u'cmd_motor',
    #u'cmd_steer',
    u'drive_mode',
    u'encoder',
    #u'encoder_meo',
    u'gyro_heading_x',
    #u'gyro_heading_x_meo',
    #u'gyro_heading_y',
    #u'gyro_heading_y_meo',
    #u'gyro_heading_z',
    #u'gyro_heading_z_meo',
    u'gyro_x',
    #u'gyro_x_meo',
    u'gyro_y',
    #u'gyro_y_meo',
    u'gyro_z',
    #u'gyro_z_meo',
    #u'human_agent',
    u'left_ts_deltas',
    u'motor',
    #u'place_choice',
    #u'right_ts',
    u'steer',
    #u'ts',
]

max_steps = 500
P = {}

P['index'] = 11000
for t in topics:
    P[opj(t,'data')] = None#zeros((1,2))
    P[opj(t,'min')] = -0.1#2**16
    P[opj(t,'max')] = 0.1#-2**16



cat = zeros((1,2))
def update(P):
    index = P['index']
    for t in topics:
        value = L[t][index]
        if value > P[opj(t,'max')]:
            P[opj(t,'max')] = value
        if value < P[opj(t,'min')]:
            P[opj(t,'min')] = value
        cat[0,0] = index
        cat[0,1] = value
        if P[opj(t,'data')] == None:
            P[opj(t,'data')] = cat
        else:
            P[opj(t,'data')] = np.concatenate((P[opj(t,'data')],cat),0)
        if len(P[opj(t,'data')]) > max_steps:
            P[opj(t,'data')] = P[opj(t,'data')][-max_steps:,:]
    P['index'] += 1
    Hz.freq()

img = image.get_blank_image(500,500) #########

#cs = z55(np.random.randn(len(P[opj(t,'data')]),3))
#cs *= 0
#for i in range(3):
#    cs[:,i] = 255
plot_timer = Tr(2/30)
message = Tr(3)
tr = Tr(500)
Hz=Tr(3)
while not tr.c():
    #message.message(d2s(P['acc_x/min'],P['acc_x/max']))
    
    if True:#:try:
        for i in range(2):
            update(P)
        if True:#plot_timer.c():
            plot_timer.reset()
            ctr = 0
            for t in topics:
                #print t
                ctr += 1
                cs = zeros((len(P[opj(t,'data')]),3))+255

                xys = image.get_float_pixels( #########
                    xys=na(P[opj(t,'data')]),
                    img_shape=shape(img),
                    col=(1,1),
                    row=(len(topics)-ctr+1,len(topics)),
                    box=((0,len(P[opj(t,'data')])),(P[opj(t,'min')],P[opj(t,'max')]))
                )
                image.img_pts_plot(img,xys,cs) #########
            mci(img)
            img *= 0

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            



    """
    mci(img)
    img *= 0
    if imgtimer.check():
        rr=1+np.random.randint(5)
        rc=1+np.random.randint(5)
        imgtimer.reset()
    image.place_image_in_image2(img,b,row=(rr,5),col=(rc,5)) #########
    
    s = 0.95
    MX = s*MX + (1-s)*(MX-MN)/2.0
    MN = s*MN + (1-s)*(MX-MN)/2.0
    """

#EOF
