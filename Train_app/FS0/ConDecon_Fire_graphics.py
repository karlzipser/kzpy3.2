from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None



def graphics_function(N,target):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(5)
    cv2.waitKey(1)
    
    if graphics_timer.check():
        graphics_timer = Timer(5)
    else:
        return

    c = N.extract('camera_input')[:3,:,:]
    #t = N.extract('target')[:3,:,:]
    t = target[0,:,:,:]
    d = N.extract('final_output')[:3,:,:]

    img = np.concatenate((d.transpose(2,1,0),d.transpose(2,1,0)),axis=1)
    mci(z55(img),1,scale=4,title='target')

    spause()


#EOF
