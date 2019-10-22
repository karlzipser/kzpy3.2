def backup_folder(
	src=opjh('kzpy3'),
	dst=opjh('__kzpy3_older','kzpy3_'+time_str())+'/'
	):
	"""
	Make a time marked backup, with default as kzpy3.
	"""
    os.system('mkdir -p ' + dst)
    os.system(d2s('cp -r',src,dst))


