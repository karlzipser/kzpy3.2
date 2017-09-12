#!/usr/bin/env python

from kzpy3.utils2 import *
import kzpy3.Cars.robot_car_1Sept2017.nodes.runtime_parameters as rp
A = 170
B = 500

Car_xterm_colors_dic = {'Mr_Blue':('white','blue',(0,0)),
	'Mr_Black':('white','black',(0,A)),
	'Mr_Orange':('white','red',(0,2*A)),
	'Mr_Yellow':('black','yellow',(B,0)),
	'Mr_Lt_Blue':('black','cyan',(B,A)),
	'Mr_Purple':('white','purple',(B,2*A)),
}
ctr = 0
second_row = 0
for k in sorted(Car_xterm_colors_dic.keys()):
	a = Car_xterm_colors_dic[k][2][1]
	b = Car_xterm_colors_dic[k][2][0]
	fg = Car_xterm_colors_dic[k][0]
	bg = Car_xterm_colors_dic[k][1]
	for geo in [d2n('80x10+',b,'+',a),d2n('20x5+',int(2.2*B),'+',int(0.6*ctr*A))]:
		ssh = d2n('ssh nvidia@',rp.Car_IP_dic[k])
		os.system(d2s('xterm -hold -geometry',geo,'-bg',bg,'-fg',fg,'-e ',ssh,'&'))
	ctr += 1