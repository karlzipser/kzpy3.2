from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None
#W = {}

def graphics_function(N,M,P):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
        #W['display.input'] = P['display.input']
        #W['display.output'] = P['display.output']
        #W['display.target'] = P['display.target']

    cv2.waitKey(1)
    if graphics_timer.check() or M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
        if M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
            pass
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    title_name = title='.'.join(P['type'])

    if True:
        
        figure(P['type'][-1],figsize=(2,10))
        clf()
        plot(N.losses,'.')
        m = meo(na(N.losses),M['Q']['runtime_parameters']['meo_num'])
        plot(m)
        mm = na(m[int(len(m)/2):])
        #kprint(shape(mm),'shape(mm)')
        if len(mm) > 5 :
            #kprint(shape(mm),'shape(mm)')
            mx = mm.max() * 1.3
            mn = mm.min() * 0.8
            ylim(
                mn,#M['Q']['runtime_parameters']['graphics_ylim'][0],
                mx,#M['Q']['runtime_parameters']['graphics_ylim'][1]
            )


    #P['display.output'] = [0,3,3,6]
    #P['display.target'] = [0,3,3,6]
    #P['display.input'] = [3,6]



    Imgs = {}
    img_lst = []
    for k in ['input','target','output']:
        Imgs[k] = N.extract(k)
        #print k,Imgs[k].min(),Imgs[k].max()
        lst = P['display.'+k]
        for i in range(0,len(lst),2):
            start = int(lst[i])
            stop = int(lst[i+1])
            img = Imgs[k][start:stop,:,:]
            img = z55(img.transpose(2,1,0))
            #mci(img,title=d2s(k,start,stop),scale=4)
            img_lst.append(img)
    #kprint(W)
    concatt = None
    while len(img_lst) > 0:
        img = img_lst.pop(0)
        if type(concatt) == type(None):
            concatt = img.copy()
            #print 'a',shape(concatt),shape(img)
        else:
            #print 'b',shape(concatt),shape(img)
            concatt = np.concatenate((concatt,img),axis=1)
    mci(concatt,1,scale=M['Q']['runtime_parameters']['scale'],title=title_name)
    #cv2.moveWindow(title_name,P['win_x'],P['win_y'])
    #mci(concatt,1,scale=2,title=d2s('concat'))



    if M['Q']['runtime_parameters']['save_images']:
        path = opjD('__TEMP__',fname(P['NETWORK_OUTPUT_FOLDER']))
        print path
        os.system(d2s('mkdir -p',path))
        imsave(opj(path,str(time.time())+'.png'),img)


    spause()


#EOF
