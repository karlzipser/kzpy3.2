
from kzpy3.utils2 import *
Car_ips = {'Mr_Silver':'192.168.1.10','Mr_Gold':'192.168.1.14'}
this_car = os.environ["COMPUTER_NAME"]
if this_car == 'Mr_Silver':
	other_car = 'Mr_Gold'
else:
	other_car = 'Mr_Silver'
timer = Timer(0)
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(Car_ips[other_car], username='nvidia',password='nvidia')
timer = Timer(0)
for i in range(1000):
	ssh.exec_command(d2n("echo '(1.4,5.2,",i,")' > ~/Desktop/",other_car,".txt "))
	print(i,dp(i/timer.time()))












#EOF