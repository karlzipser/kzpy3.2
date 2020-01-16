from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None


def graphics_function(N,M,P):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    cv2.waitKey(1)
    if graphics_timer.check() or M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
        if M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
            pass
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    if True:
        figure('loss')
        clf()
        plot(N.losses,'.')
        m = meo(na(N.losses),M['Q']['runtime_parameters']['meo_num'])
        plot(m)
        ylim(
            M['Q']['runtime_parameters']['graphics_ylim'][0],
            M['Q']['runtime_parameters']['graphics_ylim'][1]
        )


        
    cc = N.extract('input')
    tt = N.extract('target')
    dd = N.extract('output')
    t = tt[:3,:,:]
    d = dd[:3,:,:]
    c = cc[:3,:,:]
    img = np.concatenate((z55(c.transpose(2,1,0)),z55(d.transpose(2,1,0)),z55(t.transpose(2,1,0))),axis=1)
    mci(z55(img),1,scale=4,title=d2s('input/output/target (channels 0-2)',shape(dd)))

#    print shape(tt)
    if False:#shape(tt)[0] == 6:
        t = tt[3:,:,:]
        d = dd[3:,:,:]
        img = np.concatenate((d.transpose(2,1,0),t.transpose(2,1,0)),axis=1)
        mci(z55(img),1,scale=4,title=d2s('target 3-5',shape(dd)))
    if False:#shape(tt)[0] > 6:
        n = rndint(shape(tt)[0]-3)
        print shape(tt)[0],n,n+2
        t = tt[n:n+2,:,:]
        d = dd[n:n+2,:,:]
        img = np.concatenate((d.transpose(2,1,0),t.transpose(2,1,0)),axis=1)
        mci(z55(img),1,scale=4,title=d2s('target',n,'-',n+3,shape(dd)))


    if M['Q']['runtime_parameters']['save_images']:
        path = opjD('__TEMP__',fname(P['NETWORK_OUTPUT_FOLDER']))
        print path
        os.system(d2s('mkdir -p',path))
        imsave(opj(path,str(time.time())+'.png'),img)


    spause()


#EOF
