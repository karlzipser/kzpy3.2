from kzpy3.utils2 import *

def get_marker_xy_dic():

	marker_spacing_ = 107/4.0/100.0
	marker_width = 21/100.0

	Markers_clockwise = {
		################
		# East 1
		'East':[ 51,50,4,63,
			# East 2
			146,147,148,149,
			# East 3
			52,189,192,191,
			# East 4
			199,200,202,203],
			#
		################
		# South 1
		'South':[204,205,208,206,
			# South 2
			174,175,176,177,
			# South 3
			57,58,67,59,
			# South 4
			173,172,171,170],
		################
		# West 1
		'West':[227,226,228,225,
			# West 2
			153,152,151,150,
			# West 3
			134,133,139,138,
			# West 4
			216,217,218,219],
		#################
		# North 1
		'North':[223,222,221,220,
			# North 2
			132,137,136,135,
			# North 3
			198,196,197,194,
			# North 4
			178,179,180,181]
			###############
	}

	Marker_xy_dic = {}

	ctr_ = 7.5
	for k_ in Markers_clockwise['North']:
		Marker_xy_dic[k_] = na([ctr_*marker_spacing_,-8*marker_spacing_])
		Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([marker_width/2.0,0])
		Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] - na([marker_width/2.0,0])
		ctr_ -= 1
	ctr_ = -7.5
	for k_ in Markers_clockwise['South']:
		Marker_xy_dic[k_] = na([ctr_*marker_spacing_,8*marker_spacing_])
		Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] - na([marker_width/2.0,0])
		Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([marker_width/2.0,0])
		ctr_ += 1
	ctr_ = -7.5
	for k_ in Markers_clockwise['East']:
		Marker_xy_dic[k_] = na([-8*marker_spacing_,ctr_*marker_spacing_])
		Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([0,-marker_width/2.0])
		Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([0,marker_width/2.0])
		ctr_ += 1
	ctr_ = 7.5
	for k_ in Markers_clockwise['West']:
		Marker_xy_dic[k_] = na([8*marker_spacing_,ctr_*marker_spacing_])
		Marker_xy_dic[(k_,left)] = Marker_xy_dic[k_] + na([0,marker_width/2.0])
		Marker_xy_dic[(k_,right)] = Marker_xy_dic[k_] + na([0,-marker_width/2.0])
		ctr_ -= 1

	Marker_xy_dic[100] = na([-0.21,-0.82])
	Marker_xy_dic[0] = na([-0.21,-0.84-marker_width])
	Marker_xy_dic[11] =  na([-0.12,-0.12]) + Marker_xy_dic[100]
	Marker_xy_dic[102] = na([0.12,-0.11]) + Marker_xy_dic[100]

	for side_ in [left,right]:
		for m_ in [100,0,102,11]:
			Marker_xy_dic[m_,side_] = Marker_xy_dic[m_].copy()

	Marker_xy_dic[(100,right)] += na([marker_width/2.0,0])
	Marker_xy_dic[(100,left)] -= na([marker_width/2.0,0])
	Marker_xy_dic[(0,left)] += na([marker_width/2.0,0])
	Marker_xy_dic[(0,right)] -= na([marker_width/2.0,0])
	Marker_xy_dic[(11,right)] += na([0,marker_width/2.0])
	Marker_xy_dic[(11,left)] -= na([0,marker_width/2.0])
	Marker_xy_dic[(102,left)] += na([0,marker_width/2.0])
	Marker_xy_dic[(102,right)] -= na([0,marker_width/2.0])

	return Marker_xy_dic


Marker_xy_dic = get_marker_xy_dic()

