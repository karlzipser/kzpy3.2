from kzpy3.utils3 import *

timer = Timer(0.1)
total_timer = Timer()
raw_enter(' other.py ')

while True:
	if timer.check():
		timer.reset()
		soD('a',
			{
				'df':percent_disk_free('/'),
				'memory':memory(),
				'time':dp(total_timer.time())
			},
		)
	else:
		time.sleep(0.1)
		continue