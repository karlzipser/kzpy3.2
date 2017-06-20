from kzpy3.utils import *

import paramiko

def get_sftp(pw_file_path):
	hup = txt_file_to_list_of_strings(pw_file_path)
	host = hup[0]
	port = 22
	transport = paramiko.Transport((host, port))
	password = hup[2]
	username = hup[1]
	transport.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)
	return sftp

hup = txt_file_to_list_of_strings('/Users/karlzipser/pw_RPi.txt')# '/Users/karlzipser/pw_MacbookPro.txt')
