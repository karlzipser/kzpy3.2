







from kzpy3.utils2 import *
###################### left-right ts dic ####################
#

car = Args['CAR_NAME']
folders5 = sgg('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py/*')
for f in folders5:
	if car in f:
		try:
			F=h5r(opj(f,'original_timestamp_data.h5py'))
			print fname(f)
			r = F['right_image']['ts']
			l = F['left_image']['ts']
			left_right_dic = {}
			for i in range(len(l)):
				t = l[i]
				for j in range(max(0,i-10),min(i+10,len(r))):
					if r[j] > t and r[j] < t+0.1:
						left_right_dic[t] = r[j]
						break
			so(left_right_dic,opj(f,'left_right_ts_dic'))
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)			
			




#EOF