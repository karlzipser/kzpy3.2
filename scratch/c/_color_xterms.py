from kzpy3.utils2 import *
import kzpy3.Cars.robot_car_1Sept2017.nodes.runtime_parameters as rp

Car_xterm_colors_dic = {'Mr_Blue':('white','blue'),
	'Mr_Black':('white','black'),
	'Mr_Orange':('white','red'),
	'Mr_Yellow':('black','yellow'),
	'Mr_Lt_Blue':('black','cyan'),
	'Mr_Purple':('white','purple'),
}
ctr = 0
for k in Car_xterm_colors_dic:
	for geo in [d2n('80x10+0+',ctr*180),d2n('20x10+600+',ctr*180)]:
		fg = Car_xterm_colors_dic[k][0]
		bg = Car_xterm_colors_dic[k][1]
		ssh = d2n('ssh nvidia@',rp.Car_IP_dic[k])
		os.system(d2s('xterm -hold -geometry',geo,'-bg',bg,'-fg',fg,'-e ',ssh,'&'))
	ctr += 1