#!/usr/bin/python

from kzpy3.utils3 import *

if False:
	for i in range(0,256):
		ip = d2p(192,168,1,i)
		unix_str = d2s('ping -c 2 -W 0.2',ip)
		pd2s(unix_str)
		unix(unix_str)
		#time.sleep(3)

if False:
	import os
	hostname = "192.168.1.13" #example
	response = os.system("ping -c 3 " + hostname+' &')
	print response

	#and then check the response...
	if response == 0:
	  print hostname, 'is up!'
	else:
	  print hostname, 'is down!'

if True:
	H = {}

	def ping_test(hostname):
		print hostname
		response = os.system("ping -c 10 " + hostname)
		if response == 0:
			H[hostname] = 1
			pd2s(hostname,'is','up')
		else:
			H[hostname] = 0

	for i in range(10,14):
		#hostname = d2p(169,254,131,i)
		hostname = d2p(192,168,1,i)
		threading.Thread(target=ping_test,args=[hostname]).start()
"""
if False:
	import multiprocessing.dummy
	import multiprocessing

	def ping(ip):
	   success = 0# Run the ping command here
	   if success:
	       print("{} responded".format(ip))
	   else:
	       print("{} did not respond".format(ip))
	   return success

	def ping_range(start, end):
	    num_threads = 2 * multiprocessing.cpu_count()
	    p = multiprocessing.dummy.Pool(num_threads)
	    p.map(ping, [10.0.0.x for x in range(start,end)])

	if __name__ == "__main__":
	    ping_range(0, 255)
"""


