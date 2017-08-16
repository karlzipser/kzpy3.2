from kzpy3.vis import *
import cv2
import sys

haarPath = '/usr/local/Cellar/opencv/2.4.12/share/OpenCV/haarcascades'
face_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_eye.xml')
body_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_fullbody.xml')


def face_detect_from_video(video_capture,scaleFactor=1.1):
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces,eyes = face_detect(gray,scaleFactor)
    return faces,eyes,frame


def face_detect_from_file(path_filename,scaleFactor=1.1):
    frame = cv2.imread(path_filename)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces,eyes = face_detect(gray,scaleFactor)
    return faces,eyes,frame


def face_detect(gray,scaleFactor):
	faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=scaleFactor,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
	eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=scaleFactor,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
	return faces,eyes


def visualize_face_detect_from_video(scaleFactor=1.1):
	video_capture = cv2.VideoCapture(0)

	while True:
	    faces,eyes,frame = face_detect_from_video(video_capture)
	    for (x,y,w,h) in faces:
	        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	    for (x,y,w,h) in eyes:
	        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
	    cv2.imshow('Video', np.fliplr(scipy.misc.imresize(frame,25)))
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
	video_capture.release()
	cv2.destroyAllWindows()


def visualize_face_detect_from_file(path_filename,scaleFactor=1.1,fig_name='face detection'):
	faces,eyes,frame = face_detect_from_file(path_filename,scaleFactor)
	xwid = shape(frame)[1]
	ywid = shape(frame)[0]
	i = 0
	for things in [faces]:
		for i in range(len(things)):
		    x0 = things[i,0]
		    y0 = things[i,1]
		    xw = things[i,2]
		    yw = things[i,3]
		    w = np.round((xw+yw)/2.0)
		    x1 = np.max([0,x0-w])
		    y1 = np.max([0,y0-w])
		    x2 = np.min([xwid-1,x0+2*w])
		    y2 = np.min([ywid-1,y0+2*w])
		    f = frame[y0:y0+w,x0:x0+w]
		    f = imresize(f,[256,256],'bilinear')
		    mi(f,d2s(fig_name,i))
	mi(frame,d2s(fig_name,i+1))

