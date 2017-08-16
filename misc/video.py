from kzpy3.utils import *

import cv2

"""
desired_output_width:
    we assume video is in landscape orientation.
"""
def video_to_frames(video_path,video_filename,desired_output_width,frames_per_folder=1000):
    video_fpath = opj(video_path,video_filename)
    video_frames_fpath = opj(video_path,'frames')
    cap = cv2.VideoCapture(video_fpath)
    subfolder = 0
    start_time = time.time()
    ctr = 0
    fctr = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            if ctr == 0:
                scale_ratio = 1.0/(shape(frame)[0]/(1.0*desired_output_width))
                new_size = [desired_output_width,np.int(np.round(scale_ratio*shape(frame)[1]))]
                unix(d2s('mkdir -p', opj(video_frames_fpath,str(subfolder))))
            #print(ctr,subfolder)
            frame = imresize(frame,new_size)
            cv2.imwrite(opj(video_frames_fpath,str(subfolder),str(ctr)+'.jpg'),frame,[int(cv2.IMWRITE_JPEG_QUALITY), 90])
            #cv2.imwrite('img_CV2_90.jpg', a, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            ctr += 1
            if ctr % frames_per_folder == 0:
                subfolder += frames_per_folder
                unix(d2s('mkdir -p', opj(video_frames_fpath,str(subfolder))))
                fctr += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    print(d2s('Saved',ctr,'frames in',fctr,'folders in ',np.int(time.time()-start_time),'seconds'))
    cap.release()
    #cv2.destroyAllWindows()
"""
frame to video is not working, but here are alternatives:
    
    ffmpeg -r 15 -i %d.jpg -vcodec mpeg4 -b 990k video.avi
    [see http://stackoverflow.com/questions/3158235/image-sequence-to-video-quality]

    
    [see http://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality]
    ffmpeg  -r 15 -i %d.jpg output.gif
"""

def frame_to_video(img_folder):
    video = cv2.VideoWriter('video.avi',-1,1,(298,224))
    img_filenames = sorted(gg(opj(img_folder,'*.*')),key=natural_keys)
    for i in range(len(img_filenames)):
        print(d2n(i,') ',img_filenames[i]))
        img = cv2.imread(img_filenames[i])
        video.write(img)
    cv2.destroyAllWindows()
    video.release()


