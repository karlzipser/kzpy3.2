import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='',password='')
stdin,stdout,stderr = ssh.exec_command('pwd;cd ~/Desktop;ls -al;pwd')
print(stdout.read())
stdin,stdout,stderr = ssh.exec_command('pwd;cd ~/Desktop;ls -al;pwd;cp image10.png temp;cd temp;ls -al');print(stdout.read())

import time
import picamera
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
for i in range(1000):
	camera.capture('image1.jpg',quality=5)
	time.sleep(0.4)




import paramiko
paramiko.util.log_to_file('/tmp/paramiko.log')

# Open a transport

host = "example.com"
port = 22
transport = paramiko.Transport((host, port))

# Auth

password = "foo"
username = "bar"
transport.connect(username = username, password = password)

# Go!

sftp = paramiko.SFTPClient.from_transport(transport)

# Download

filepath = '/etc/passwd'
localpath = '/home/remotepasswd'
sftp.get(filepath, localpath)

# Upload

filepath = '/home/foo.jpg'
localpath = '/home/pony.jpg'
sftp.put(localpath, filepath)

# Close

sftp.close()
transport.close()