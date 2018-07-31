###################################################################
# https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73

while True:
	try:
		from kzpy3.utils2 import *
		import paramiko
		sshclient = paramiko.SSHClient()
		sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		sshclient.connect('192.168.1.12',username='nvidia')
		freq_timer = Timer(0.5)
		ready = '.ready'
		done = '.done'
		path = '/home/nvidia/Desktop/paramiko/'
		for i in range(300):
			new_file = d2n(i,'.',i+1)
			sshclient.exec_command(d2n('rm ',path,'*'+done,';   touch ',path,new_file+ready))
			#sshclient.exec_command(d2n('mv ',path,new_file+ready,'   ',path,new_file+done))
			#sshclient.exec_command(d2n('rm ',path,'*'+ready))
			print i
			time.sleep(.00001)
			freq_timer.freq()


		freq_timer.reset
		timer=Timer(30)
		while not timer.check():
			stdin,stdout,stderr=sshclient.exec_command('ls '+path)
			LS = stdout.read()
			LS = LS.replace('/',',')
			print(LS)
			freq_timer.freq()
	except:
		print 'paramiko failed'
		time.sleep(1)










def paramiko_connection_thread():
	timer = Timer(0)
	while timer.time() < 120:
		try:
			sshclient.connect(rp.Car_IP_dic[k], username='nvidia')
			Connected_car_names[k] = True
			spd2s('ssh connection to',k,'established')
			break
		except:
			pd2s('ssh connection to',k,'failed')
			time.sleep(5)
threading.Thread(target=paramiko_connection_thread).start()

ssh_command_str = d2s('cp',opjD('test.txt'))

temp = d2n("echo 'pose = ",pose_str,"\nxy = ",xy_str,"\nheading_floats = ",heading_floats_str,"' > ~/Desktop/",rp.computer_name,".car.txt ")
ssh_command_str = temp
				
error_timer = Timer(1)

# test rate
def paramiko_command_thread():
	timer = Timer(0)
	while True:

		try:
			sshclient.exec_command(ssh_command_str)
			#spd2s('ssh.exec_command  to',k)
		except:
			if error_timer.check():
				srpd2s('ssh.exec_command failed to',k)
				error_timer.reset()
		t = timer.time()
		if t < 0.1:#one_over_sixty:
			time.sleep(0.1-t) #one_over_sixty - t)

threading.Thread(target=paramiko_command_thread).start()
#
###################################################################