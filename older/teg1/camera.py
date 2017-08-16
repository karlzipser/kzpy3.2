from kzpy3.utils import *

def camera_on(data_dir=opjD('teg_data/temp')):
	"""Make data dir, change to that dir, start camera, then return to start dir."""
	unix('mkdir -p ' + data_dir)
	current_dir = os.getcwd()
	os.chdir(data_dir)
	subprocess.Popen([opjh('kzpy3/teg1/cam15Hz320x240.sh')])
	os.chdir(current_dir)

def camera_off():
	"""
	On my first TX1, this worked fine, but on the second it became unreliable.
	Therefore, I am disabling the camera off altogether.
	"""
	if  False:
		kill_ps('gst-launch-1.0') # TX1
		#kill_ps('gst-launch-0.10') #TK1

