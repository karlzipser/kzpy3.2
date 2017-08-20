# https://askubuntu.com/questions/87665/how-do-i-change-the-hostname-without-a-restart
# sudo hostname your-new-name

# https://askubuntu.com/questions/224559/how-to-find-all-the-used-ip-addresses-on-a-network
# https://nmap.org/download.html#macosx
# nmap -sn 192.168.1.0/24

# https://www.turnkeylinux.org/node/41
#ifconfig eth0 192.168.0.10 netmask 255.255.255.0 up

#https://pricklytech.wordpress.com/2013/04/24/ubuntu-change-hostname-permanently-using-the-command-line/
from kzpy3.utils2 import *
import threading

Computers = {
	'ubuntu_laptop2':	'192.168.1.100',
	'Mr_Blue':			'192.168.1.101',
	'Mr_Black':			'192.168.1.102',
	'Mr_Orange':		'192.168.1.103',
	'Mr_Yellow':		'192.168.1.104',
	'Mr_Lt_Blue':		'192.168.1.105',
	'Mr_Purple':		'192.168.1.106',
	'iMac':				'192.168.1.39',
	}

Computers_online = {}

def ping_test(*args):
	"""
	Args[IP_ADDRESS]
	"""
	Args = args_to_dictionary(args)
	True
	result = unix(d2n('sudo ping -c 1 -W 0.3 -i 0.2 ',Args[IP_ADDRESS]))
	for i in rlen(result):

		if 'transmitted' in result[i]:
			#print result
			num_str = result[i].split('transmitted')[1].split(' ')[1]
			#print num_str
			return int(num_str)

def ping_status():
	print('ping status:')
	for k in sorted(Computers_online):
		print(d2n('\t',k,' (',Computers[k],') ',dp(time.time()-Computers_online[k],2),' s ago'))

STOP_PING_TEST_THREAD = 'STOP_PING_TEST_THREAD'
P = {}
P[STOP_PING_TEST_THREAD] = False

def ping_test_thread():
	while True:
		if P[STOP_PING_TEST_THREAD]:
			return
		for k in sorted(Computers):
			if ping_test(IP_ADDRESS,Computers[k]):
				Computers_online[k] = time.time()

threading.Thread(target=ping_test_thread).start()