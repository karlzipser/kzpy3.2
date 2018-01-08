from kzpy3.vis2 import *

data_path = Args['PATH']


#data_path = '/home/karlzipser/Desktop/bdd_car_data_14Sept2017_circle'
ctr = 0
display_timer = Timer(1)
heading_pause_data_moments = []
folders = sggo(data_path,'h5py/*')
for f in folders:
	try:
		left_timestamp_index_dic = lo(opj(f,'left_timestamp_index_dic'))
		right_timestamp_index_dic = lo(opj(f,'right_timestamp_index_dic'))
		left_right_ts_dic = lo(opj(f,'left_right_ts_dic'))
		"""
		if len(gg(opj(f,'left_timestamp_metadata_right_ts.h5py'))) > 0:
			L = h5r(opj(f,'left_timestamp_metadata_right_ts.h5py'))
		else:
			L = h5r(opj(f,'left_timestamp_metadata.h5py'))
		"""
		L = h5r(opj(f,'aruco_position.h5py'))
		O = h5r(opj(f,'original_timestamp_data.h5py'))

		modified_heading_pause = 0*L['heading_pause'][:]
		for i in range(1,len(modified_heading_pause)):
			modified_heading_pause[i]=L['heading_pause'][i]*(modified_heading_pause[i-1]+1)
		modified_heading_pause[modified_heading_pause>30]=0 # i.e., heading pause only up to one second.


		try:
			for i in rlen(L['ts'][:]):
				if i < len(modified_heading_pause):
					if modified_heading_pause[i] > 0:
						name = fname(f)
						t = L['ts'][i]
						rt = left_right_ts_dic[t]
						#rt = L['right_ts'][i]
						for cc in [0,1]:
							for mode in ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']:
								heading_pause_data_moments.append({'run_name':name,'left_ts_index':(t,left_timestamp_index_dic[t]),'right_ts_index':(rt,right_timestamp_index_dic[rt]),'behavioral_mode':mode,'counter_clockwise':cc,'steer':49,'motor':49,'other_car_in_view':True})
								#heading_pause_data_moments.append([name,((t,left_timestamp_index_dic[t]),(rt,right_timestamp_index_dic[rt])),(mode,cc),(49,49)])
						if display_timer.check():
							if i < len(O['left_image']['vals']):
								mi(O['left_image']['vals'][i]);spause()
								display_timer.reset()
		except Exception as e:
			print("********** 1 Exception ***********************")
			print(e.message, e.args)
			#if len(heading_pause_data_moments) > 1000:
			#	break
		#if len(heading_pause_data_moments) > 1000:
		#	break
		L.close()
		O.close()
	except Exception as e:
		print("********** 2 Exception ***********************")
		print(e.message, e.args)
so(heading_pause_data_moments,opj(data_path,'heading_pause_data_moments_indexed'))
						
