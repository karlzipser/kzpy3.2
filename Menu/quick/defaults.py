from kzpy3.utils3 import *

current_car = 'j26June2019'
Q = {
    '--mode--':'bash',
    '.tx_connect_2.py': d2s('python',opjk('scripts/connect/tx_connect_2.py')),
    '.......Grapher/main.py': d2s('python',opjk('Grapher/main.py')),
    '....arduino_node.py':	d2s('python',opjk('Cars',current_car,'nodes','arduino_node.py')),
    '.....control_node.py':	d2s('python',opjk('Cars',current_car,'nodes','control_node.py')),
    '......network_node.py':	d2s('python',opjk('Cars',current_car,'nodes','network_node.py')),
    '...car menu':	d2s('python',opjk('Menu_app/menu2.py'),'--path',opjk('Cars',current_car,'nodes'),'--dic P'),
	'..Mr_New 169.254.131.242':'ssh -X nvidia@169.254.131.242',
	'..Mr_Purple 169.254.131.243':'ssh -X nvidia@169.254.131.243',
}
#for k in sorted(Q.keys()):
#	cg(Q[k])

#EOF
