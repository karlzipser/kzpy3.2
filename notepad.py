# 

def get_heading_centers(*args):
	Args = args_to_dictionary(args)
	Cs = lo(Args[aruco_cubic_splines])
	L = h5r(Args[left_timestamp_metadata])

	D = {}
	D[ts] = L[ts][:]
	D[motor] = L[motor][:]
	D[steer] = L[steer][:]
	D[state] = L[state][:]

	good_ts_ = []
	good_ts_indicies_ = []
	for i_ in rlen(D[ts]):
		t_ = D[ts][i_]
		if D[motor][i_] > 49:
			if D[state][i_] == 1:
				good_ts_.append(t_)
				good_ts_indicies_.append(i_)
	good_ts_ = na(good_ts_)
	good_motor_ = D[motor][good_ts_indicies_]
	good_steer_ = D[steer][good_ts_indicies_]


	x_ = (Cs[left][x_meo](good_ts_)+Cs[right][x_meo](good_ts_))/2.0
	y_ = (Cs[left][y_meo](good_ts_)+Cs[right][y_meo](good_ts_))/2.0
	figure(1)
	plot(good_ts_,x_,'.')
	plot(good_ts_,y_,'.')
	figure(2);clf();plt_square();xysqlim(2*107.0/100.0);
	plot(x_[100:],y_[100:],'.')

	hx_ = (Cs[left][hx_meo](good_ts_)+Cs[right][hx_meo](good_ts_))/2.0-(Cs[left][x_meo](good_ts_)+Cs[right][x_meo](good_ts_))/2.0
	hy_ = (Cs[left][hy_meo](good_ts_)+Cs[right][hy_meo](good_ts_))/2.0-(Cs[left][y_meo](good_ts_)+Cs[right][y_meo](good_ts_))/2.0

	figure(3)
	plot(good_ts_,hx_,'.')
	plot(good_ts_,hy_,'.')

	angle_clockwise_ = []
	for i_ in rlen(hx_):
		angle_clockwise_.append(angle_clockwise((0,1),(hx_[i_],hy_[i_])))
	angle_clockwise_ = na(angle_clockwise_)
	figure(4)
	plot(good_ts_,angle_clockwise_,'.')


	figure(5);clf();plt_square();xysqlim(2*107.0/100.0)
	for an_ in range(15,180+15,30):
		ox_=[];oy_=[]
		
		for i_ in range(0,len(hx_),5):
			if angle_clockwise_[i_] > an_-15 and angle_clockwise_[i_]<an_+15:
				ox_.append(x_[i_])
				oy_.append(y_[i_])
		plot(ox_,oy_,'.');spause()

	return {steer:good_steer_, motor:good_motor_, ts:good_ts_, angle:angle_clockwise_, x:x_, y:y_}



Heading_centers = get_heading_centers(
	left_timestamp_metadata,opjD('bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_17h39m41s_Mr_Yellow/left_timestamp_metadata.h5py'),
	aruco_trajectories,opjD('meta/direct_home_LCR_Aruco1_23Jul17_17h39m41s_Mr_Yellow/Aruco_trajectories.h5py'),
	aruco_cubic_splines,opjD('meta/direct_home_LCR_Aruco1_23Jul17_17h39m41s_Mr_Yellow/Cubic_splines.pkl'))
