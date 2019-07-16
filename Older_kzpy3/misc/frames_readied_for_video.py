from kzpy3.utils import *
from kzpy3.misc.progress import *

def frames_to_video_with_ffmpeg(input_dir,img_range=()):
	if input_dir[-1] == '/':
		input_dir = input_dir[:-1] # the trailing / messes up the name.
	_,fnames = dir_as_dic_and_list(input_dir)
	frames_folder = input_dir.split('/')[-1]
	if len(img_range) == 0:
		img_range = (0,len(fnames))
	temp_dir = opjD('temp'+'_'+frames_folder)
	unix(d2s('mkdir -p',temp_dir))
	ctr = 0
	print('setting up '+temp_dir)
	pb = ProgressBar(img_range[1])
	for i in range(img_range[0],img_range[1]):
		if np.mod(i,100) == 0:
			pb.animate(i+1)
		unix(d2s('ln -s',opj(input_dir,fnames[i]),opj(temp_dir,d2n(ctr,'.jpg'))),False)
		ctr+=1
	# note 30 fps rate. 15 fps may not be accepted, so for display this must be fixed in iMovies
	unix_str = ' -i '+temp_dir+'/%d.jpg -pix_fmt yuv420p -r 30 -b:v 14000k '+opjD(frames_folder)+'.mp4'
	success = False
	try:
		print('Trying avconv.')
		unix('avconv'+unix_str)
		success = True
	except Exception as e:
		print "'avconv did not work.' ***************************************"
		print e.message, e.args
		print "***************************************"
	if not success:
		try:
			print('Trying ffmpeg.')
			unix('ffmpeg'+unix_str)
			success = True
		except Exception as e:
			print "'ffmeg did not work.' ***************************************"
			print e.message, e.args
			print "***************************************"
	if success:
		print('frames_to_video_with_ffmpeg() had success with ' + frames_folder)
	# this works, but makes .avi which iMovie doesn't like
	#unix('ffmpeg -r 15 -i '+temp_dir+'/%d.jpg -vcodec mpeg4 -b 14000k '+opjD(frames_folder)+'.avi')



"""

o=h5r('/home/karlzipser/Desktop/all_aruco_ready/bdd_car_data_14Sept2017_whole_room/h5py/Mr_Black_2017-09-14-15-57-55/original_timestamp_data.h5py')
ctr = 1
for i in range(10000,11000):
	imsave(opjD('temp_imgs',d2n(ctr,'.png')),o[left_image][vals][i])
	ctr+=1
"""


"""
L=h5r('/home/karlzipser/Desktop/out_0.25_2_4.h5py')
a = L['left']
b = L['ldr']
fx,fy=4.,4.
os.system(d2s('mkdir -p',opjD('temp_imgs')))
os.system(d2s('rm',opjD('temp_imgs','*.png')))
ctr = 1
for i in range(0,len(a)/100):
	e = cv2.resize(b[i,:,:,:], (168,94), interpolation=0)
	f = a[i,:,:,:]
	g = np.concatenate((f,e[94/2:,:,:]),axis=0)
	imsave(opjD('temp_imgs',d2n(ctr,'.png')),g)
	ctr+=1
os.system("ffmpeg -i ~/Desktop/temp_imgs/%d.png -pix_fmt yuv420p -r 30 -b:v 14000k ~/Desktop/temp.mpg")

"""
if False:
	L=h5r('/home/karlzipser/Desktop/out_0.25_0_4.h5py')
	a = L['left']
	b = L['ldr']
	fx,fy=4.,4.
	os.system(d2s('mkdir -p',opjD('temp2_imgs')))
	os.system(d2s('rm',opjD('temp2_imgs','*.png')))
	os.system(d2s('rm',opjD('temp2.mpg')))
	ctr = 1
	len_a = len(a)
	timer = Timer(5)
	for i in range(0,len(a)):
		timer.message(d2s(i))
		e = cv2.resize(b[i,:,:,:], (168,94), interpolation=0)
		f = a[i,:,:,:].copy()
		for x in range(168):
			for y in range(94):
				if max(e[y,x,:])>0:
					f[y,x,:]=e[y,x,:]
		#g = np.concatenate((f,e[94/2:,:,:]),axis=0)
		#mi(f);spause();raw_enter()
		imsave(opjD('temp2_imgs',d2n(ctr,'.png')),f)
		ctr+=1
	os.system("ffmpeg -i ~/Desktop/temp_imgs/%d.png -pix_fmt yuv420p -r 30 -b:v 14000k ~/Desktop/temp2.mpg")	


"""
ffmpeg  -r 15 -i %d.jpg output.gif

ffmpeg -r 15 -i %d.jpg -vcodec mpeg4 -b 990k video.avi
[see http://stackoverflow.com/questions/3158235/image-sequence-to-video-quality]


ffmpeg -i %d.png -pix_fmt yuv420p -r 30 -b:v 14000k temp.mpg

"""





