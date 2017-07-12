from kzpy3.vis import *


def prepare_and_show_or_return_frame(img,steer,motor,state,delay,scale,color_mode,window_title='animate'): #,collision):
    bar_color = [0,0,0]
    if state == 1:
        bar_color = [0,0,255]
    elif state == 6:
        bar_color = [255,0,0]
    elif state == 3:
        bar_color = [200,55,0]
    elif state == 5:
        bar_color = [255,255,0]
    elif state == 7:
        bar_color = [255,0,255]
    elif state == 2:
        bar_color = [100,100,100]
    else:
        print state
        bar_color = [0,0,0]
    if steer != None:
        apply_rect_to_img(img,steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
    if motor != None:
        apply_rect_to_img(img,motor,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=False)
    #if collision == 1:
    #    img[:10,:,:] = [255,0,0] 
    if delay == None:
        scale_img = cv2.resize(img, (0,0), fx=scale, fy=scale)
        return scale_img
    else:
        k = mci(img,delay,window_title,scale)
        return k  


def animate_with_key_control(A):
    timer = Timer(1)
    ctr = 0
    while True:
        while A['STOP_ANIMATOR_THREAD'] == False:
            try:
                if len(A['images']) < 2*30:
                    print(d2s('Have',len(A['images']),'images, waiting...'))
                    time.sleep(2)
                    continue
                if timer.check():
                    print(d2s("A['current_img_index'] =", int(A['current_img_index'])))
                    timer.reset()
                A['current_img_index'] += A['d_indx']
                if A['current_img_index'] >= len(A['images']):
                    A['current_img_index'] = len(A['images'])-1
                elif A['current_img_index'] < 0:
                    A['current_img_index'] = 0
                indx = int(A['current_img_index'])
                img = A['images'][indx].copy() #.copy() # Copy if need to change image.

                if 'steer' not in A or len(A['steer']) == 0:
                    steer = 49
                    state = 0
                    motor = 49
                else:
                    steer = A['steer'][indx]
                    state = A['state'][indx]
                    motor = A['motor'][indx]
                if A['delay'] == None:
                    print('Writing to file instead of display!')
                    if len(A['images']) > A['save_stop_index']:
                        A['STOP_LOADER_THREAD'] = True
                    if A['current_img_index'] > A['save_stop_index']:
                        A['STOP_ANIMATOR_THREAD'] = True
                        A['STOP_LOADER_THREAD'] = True
                        return
                    if A['current_img_index'] >= A['save_start_index']:
                        out_img = prepare_and_show_or_return_frame(img,steer,None,state,A['delay'],A['scale'],A['color_mode'])#,A['collisions'][int(A['current_img_index'])])
                        imsave(opjD('temp2',d2n(ctr,'.png')),out_img)
                        print ctr
                        ctr += 1
                    continue
                else:
                    k = prepare_and_show_or_return_frame(img,steer,None,state,A['delay'],A['scale'],A['color_mode'])#,A['collisions'][int(A['current_img_index'])])
                if k == ord('q'):
                    print('Exiting animate_with_key_control')
                    A['STOP_GRAPH_THREAD'] = True
                    A['STOP_LOADER_THREAD'] = True
                    cv2.destroyAllWindows()
                    save_obj(A['collisions'],opjD(A['run_name']+'.collisions_'+time_str()))
                    return
                if k == ord(' '):
                    A['d_indx'] = 0
                if k == ord('1'):
                    A['d_indx'] = 1
                if k == ord('2'):
                    A['d_indx'] = 2
                if k == ord('3'):
                    A['d_indx'] = 3
                if k == ord('4'):
                    A['d_indx'] = 4
                if k == ord('5'):
                    A['d_indx'] = 7
                if k == ord('6'):
                    A['d_indx'] = 10
                if k == ord('7'):
                    A['d_indx'] = 15
                if k == ord('8'):
                    A['d_indx'] = 20
                if k == ord('9'):
                    A['d_indx'] = 30   
                if k == ord('!'):
                    A['d_indx'] = -1
                if k == ord('@'):
                    A['d_indx'] = -2
                if k == ord('#'):
                    A['d_indx'] = -3
                if k == ord('$'):
                    A['d_indx'] = -4
                if k == ord('%'):
                    A['d_indx'] = -7
                if k == ord('^'):
                    A['d_indx'] = -10
                if k == ord('&'):
                    A['d_indx'] = -15
                if k == ord('*'):
                    A['d_indx'] = -20
                if k == ord('('):
                    A['d_indx'] = -30
                if k == ord('w'):
                    print("car ahead")
                if k == ord('a'):
                    print("car left")
                if k == ord('d'):
                    print("car right")
                if k == ord('z'):
                    A['current_img_index'] = 0
                if k == ord('x'):
                    A['current_img_index'] = 1*len(A['images'])/6
                if k == ord('c'):
                    A['current_img_index'] = 2*len(A['images'])/6
                if k == ord('v'):
                    A['current_img_index'] = 3*len(A['images'])/6
                if k == ord('b'):
                    A['current_img_index'] = 4*len(A['images'])/6
                if k == ord('n'):
                    A['current_img_index'] = 5*len(A['images'])/6
                if k == ord('m'):
                    A['current_img_index'] = 6*len(A['images'])/6-1
                if k == ord('k'):
                    A['current_img_index'] -= 2*30
                if k == ord('l'):
                    A['current_img_index'] += 2*30
                if k == ord('j'):
                    while A['current_img_index'] < len(A['images']):
                        if A['acc_xz_dst'][int(A['current_img_index'])]> 7.5:
                            break
                        A['current_img_index'] += 1
                if k == ord('u'):
                    while A['current_img_index'] < len(A['images']):
                        if A['loaded_collisions'][int(A['current_img_index'])]> 0:
                            print('found collision')
                            break
                        A['current_img_index'] += 1
                if k == ord('h'):
                    if A['current_img_index'] > 12:
                        A['collisions'][int(A['current_img_index'])-12] = 1 # reaction time
            except:
                pass
                time.sleep(0.2)







def graph(A):
    figure('MSE')
    indx = int(A['current_img_index'])
    while True:
        if A['STOP_GRAPH_THREAD'] == False:   
            if len(A['images']) < 3*30:
                print(d2s('Have',len(A['images']),'images, waiting...'))
                pause(0.2)
                continue
            A_len = len(A['images'])
            clf()       
            steer = array(A['steer'])
            encoder = array(A['encoder'])
            plot(steer,'r.-')
            plot(10*encoder,'k.-')
            deltas = array(A['left_deltas'])[:,1]
            plot(deltas*100,'g')
            plot([0,len(steer)],[49,49],'k')
            t = indx
            xlim(t-30*5,t)
            motor = array(A['motor'])
            plot(motor,'b.-')
           # plot(10*A['loaded_collisions'])
            """
            N = 10

            acc_x = array(A['acc_x'])
            acc_y = array(A['acc_y'])
            acc_z = array(A['acc_z'])
            acc_x_smooth = 1.*acc_x
            for i in range(N,len(acc_x)):
                acc_x_smooth[i] = acc_x[i-N:i].mean()
            acc_y_smooth = 1.*acc_x
            for i in range(N,len(acc_y)):
                acc_y_smooth[i] = acc_y[i-N:i].mean()
            acc_z_smooth = 1.*acc_z
            for i in range(N,len(acc_z)):
                acc_z_smooth[i] = acc_z[i-N:i].mean()
            acc_xyz = 1.*acc_x_smooth
            acc_xyz[:] = sqrt(acc_x_smooth[:]**2+acc_z_smooth[:]**2)
            plot(acc_x_smooth[:],'r')
            plot(acc_y_smooth[:],'g')
            plot(acc_z_smooth[:],'b')
            plot(acc_xyz[:],'k')
            gyro_x = array(A['gyro_x'])
            gyro_y = array(A['gyro_y'])
            gyro_z = array(A['gyro_z'])
            gyro_x_smooth = 1.*gyro_x
            for i in range(N,len(gyro_x)):
                gyro_x_smooth[i] = gyro_x[i-N:i].mean()
            gyro_y_smooth = 1.*gyro_x
            for i in range(N,len(gyro_y)):
                gyro_y_smooth[i] = gyro_y[i-N:i].mean()
            gyro_z_smooth = 1.*gyro_z
            for i in range(N,len(gyro_z)):
                gyro_z_smooth[i] = gyro_z[i-N:i].mean()
            gyro_xyz = 1.*gyro_x_smooth
            gyro_xyz[:] = sqrt(gyro_x_smooth[:]**2+gyro_z_smooth[:]**2)
            plot(gyro_x_smooth[:]/10.-25,'r')
            plot(gyro_y_smooth[:]/10.-25,'g')
            plot(gyro_z_smooth[:]/10.-25,'b')
            #plot(gyro_xyz[:],'k')            
            #multi_d = sqrt( (gyro_x/50.)**2 + (gyro_y/40.)**2 + (gyro_z/30.)**2 + ((acc_x-0.5)/2.5)**2 + ((acc_y-9.8)/5)**2 + ((acc_z-0.5)/2.5)**2 ) 
            #plot(multi_d,'ko-')
            """
            ylim(-5,105)
            if False: #hist_timer.check():
                figure('left_deltas')
                left_deltas = array(A['left_deltas'])
                hist(left_deltas[:,1])
                hist_timer.reset()
                figure('MSE')
            pause(0.001)
            while A_len == len(A['images']):
                indx = int(A['current_img_index'])
                t = indx
                xlim(t-30*5,t)
                if A['STOP_GRAPH_THREAD'] == True:
                    print('Exiting graph')
                    return
                pause(0.2)
        else:
            print('Exiting graph')
            return





