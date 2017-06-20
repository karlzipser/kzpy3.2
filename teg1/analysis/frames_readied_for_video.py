from kzpy3.utils import *

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
	for i in range(img_range[0],img_range[1]):
		unix(d2s('ln -s',opj(input_dir,fnames[i]),opj(temp_dir,d2n(ctr,'.jpg'))),False)
		ctr+=1
	# note 30 fps rate. 15 fps may not be accepted, so for display this must be fixed in iMovies
	unix('ffmpeg -i '+temp_dir+'/%d.jpg -pix_fmt yuv420p -r 30 -b:v 14000k '+opjD(frames_folder)+'.mp4')
	# this works, but makes .avi which iMovie doesn't like
	#unix('ffmpeg -r 15 -i '+temp_dir+'/%d.jpg -vcodec mpeg4 -b 14000k '+opjD(frames_folder)+'.avi')


"""
ffmpeg  -r 15 -i %d.jpg output.gif

ffmpeg -r 15 -i %d.jpg -vcodec mpeg4 -b 990k video.avi
[see http://stackoverflow.com/questions/3158235/image-sequence-to-video-quality]


ffmpeg -i %d.png -pix_fmt yuv420p -r 30 -b:v 14000k temp.mpg

"""





