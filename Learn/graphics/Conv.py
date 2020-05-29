from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None
#W = {}

def graphics_function(N,M,P):#,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
        graphics_timer.trigger()

    cv2.waitKey(1)
    if graphics_timer.time_s != M['Q']['runtime_parameters']['graphics_timer_time']:
        graphics_timer.trigger()
    if graphics_timer.check() or M['Q']['runtime_parameters']['graphics_timer_time'] < 0:
        if M['Q']['runtime_parameters']['graphics_timer_time'] == -2:
            raw_enter()
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    title_name = title='.'.join(P['type'])

    if True:
        
        figure(P['type'][-1],figsize=(2,10))
        clf()

        n = int(M['Q']['runtime_parameters']['percent_loss_to_show']/100.0 * len(N.losses))
        plot(N.losses[-n:],'.')
        m = meo(na(N.losses[-n:]),M['Q']['runtime_parameters']['meo_num'])
        plot(m)
        mm = na(m[int(len(m)/2):])
        mn,mx = 0,1
        if len(M['Q']['runtime_parameters']['graphics_ylim']) == 2:
            mn = M['Q']['runtime_parameters']['graphics_ylim'][0]
            mx = M['Q']['runtime_parameters']['graphics_ylim'][1]
            #print mn,mx
        elif len(mm) > 5 :
            #av = mm.mean()
            av=0
            std = mm.std()
            #mx = (mm.max()-av) * 1.3# + av
            #mn = (mm.min()-av) * 0.8# + av
            mn = mm.mean()-std*M['Q']['runtime_parameters']['loss_stds']
            mx = mm.mean()+std*M['Q']['runtime_parameters']['loss_stds']
        #print(std,mn,mx)
        if type(mn) == float and type(mx) == float:
            ylim(
                mn,
                mx,
            )

    Imgs = {}
    img_lst = []
    img_spacer = False
    k_prev = 'input'
    for k in ['input']:#,'output','target']:
        Imgs[k] = N.extract(k)

        if 'display.'+k in P:
            lst = P['display.'+k]
            for i in range(0,len(lst),2):
                start = int(lst[i])
                stop = int(lst[i+1])
                img = Imgs[k][start:stop,:,:]
                img = z55(img.transpose(2,1,0))
                if False:#k == 'input':
                    r = img[:,:168,0].copy()
                    g = img[:,:168,1].copy()
                    b = img[:,:168,2].copy()
                    img[:,:168,0] = b
                    img[:,:168,1] = g
                    img[:,:168,2] = r

                if k_prev != k:
                    k_prev = k
                    if type(img_spacer) == type(False):
                        img_spacer = 255+0*img[:,:10,:]
                    img_lst.append(img_spacer)

                img_lst.append(img)

    figure(2);clf();
    plot(N.extract('output_2'),'r.')
    plot(N.extract('target'),'k.')
    meta = N.extract('meta')
    for i in range(5):
        mi(meta[i,:,:],i)
    spause()

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


    if M['Q']['runtime_parameters']['save_images']:
        path = opjD('__TEMP__',fname(P['NETWORK_OUTPUT_FOLDER']))
        print path
        os.system(d2s('mkdir -p',path))
        imsave(opj(path,str(time.time())+'.png'),img)


    spause()



#EOF



