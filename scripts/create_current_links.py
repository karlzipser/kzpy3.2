from kzpy3.utils import *

d = datetime.date.today()
y = str(d.year)
m = str(d.month)

mkcu = d2s('mkdir -p',opjh(y,m))
cu = d2s('ln -s',opjh(y,m),'current')

mkcgd = d2s('mkdir -p',opjh('Google_Drive',d2n(y,'-',m)))
cgd = d2s('ln -s',opjh('Google_Drive',d2n(y,'-',m)),'current_GD')

rmcu = d2s('rm',opjh('current'))
rmcdg = d2s('rm',opjh('current_GD'))
try:
	unix(rmcu,print_stdout=False, print_stderr=False,print_cmd=True)
except:
	pass
try:
	unix(rmcdg,print_stdout=False, print_stderr=False,print_cmd=True)
except:
	pass
unix(mkcu,print_stdout=False, print_stderr=False,print_cmd=True)
#unix(mkcgd,print_stdout=False, print_stderr=False,print_cmd=True)
unix(cu,print_stdout=False, print_stderr=False,print_cmd=True)
unix(cgd,print_stdout=False, print_stderr=False,print_cmd=True)
