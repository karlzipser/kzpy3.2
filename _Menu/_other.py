from kzpy3.utils3 import *

timer = Timer(0.1)

raw_enter(' other.py ')

while True:
	if timer.check():
		timer.reset()
		soD('a',{'df':percent_disk_free('/'),'memory':memory()})
	else:
		time.sleep(0.1)
		continue

#EOF
