from kzpy3.utils3 import *
import kzpy3.drafts.Log_Printer as Log_Printer

Log_printer = Log_Printer.Log_Printer(
	{
		'file__': __file__,
		'file_color': wh+on_bk,
		'color': yl,
	},
)
lp = Log_printer['print']

while True:
	time.sleep(2)
	R = lp(1,2,wh,'a',rd,time.time(),dp=3,spacer=' - ')
	cg(R)
	if R['action'] == 'ABORT':
		print('\ndone.\n')
		break
	if R['action'] == 'pause':
		print '===='
		time.sleep(1)
		continue
	print time.time()


#EOF
