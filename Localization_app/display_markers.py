SETUP = 1
SAVE = 0
RELOAD = 0
RUN_LOOP = 1
CA()

from kzpy3.Localization_app.Project_Aruco_Markers_Module import *
from kzpy3.Localization_app.aruco_whole_room_markers_11circle_no_pillar import *
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
import kzpy3.Car_Data_app.Data_Module as Data_Module
dont_know_why = True
if dont_know_why:
	P = {}
	P[VERBOSE] = True
	P[GRAPHICS] = False
	P[ROS_LIVE] = True
	P[past_to_present_proportion] = 0.99 # 0.5
	P[MARKERS_TO_IGNORE] = [190] # often has False positives
	P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
	P[ANGLE_DIST_PARAM] = 0.3




if SETUP:

	dont_know_why = True
	if dont_know_why:
		P = {}
		P[VERBOSE] = True
		P[GRAPHICS] = False
		P[ROS_LIVE] = True
		P[past_to_present_proportion] = 0.99 # 0.5
		P[MARKERS_TO_IGNORE] = [190] # often has False positives
		P[DEGREE_STEP_FOR_ROTATION_FIT] = 5#15  # 10 to 30 range, bigger is faster
		P[ANGLE_DIST_PARAM] = 0.3

	if True:
		D = Data_Module.bagfile_to_dic(BAG_PATH=opjD('bair_car_2017-10-04-14-10-17_1.bag'))#  'bair_car_2017-10-04-14-10-17_1.bag'))
		#D = Data_Module.bagfile_to_dic(BAG_PATH=opjD('processed/Mr_Purple_2017-09-29-12-20-41/bair_car_2017-09-29-12-25-45_8.bag')) #good
		#D = Data_Module.bagfile_to_dic(BAG_PATH=opjD('/home/karlzipser/Desktop/processed/Mr_Purple_2017-09-29-12-20-41/bair_car_2017-09-29-12-25-07_7.bag'))
		##D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg('/home/karlzipser/Desktop/processed/Mr_Purple_2017-09-29-12-20-41/a/*.bag'))
		#D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg(opjD('/home/karlzipser/Desktop/processed/Mr_Purple_2017-09-29-12-20-41/*.bag')))
		#D = Data_Module.bagfile_to_dic(BAG_PATH=opjD('Mr_Purple_2017-09-23-17-10-53/bair_car_2017-09-23-17-18-23_12.bag'))
		#D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg(opjD('processed/Mr_Purple_2017-09-23-17-10-53/*.bag')) ) #'Mr_Black_2017-09-12-13-48-11/a/*.bag')) )
		#D = Data_Module.bagfile_to_dic(BAG_PATH_LIST=sgg(opjD('Mr_Purple_2017-09-29-12-20-41/*.bag')) ) #'Mr_Black_2017-09-12-13-48-11/a/*.bag')) )
	if False:
		D = lo(opjD('one_bag_dic2'))


	def get_Frame_data(img_lst):
		views = 0

		print('get_Frame_data(img_lst)')
		n = len(img_lst)
		graphics = True

		timer = Timer(1)
		F = {}
		for h in range(1):
			for i in range(n):
				#print i
				try:
					mm = {}
					angles_to_center_more = {}
					angles_surfaces_more = {}
					distances_marker_more = {}
					for r in range(1):
						angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(img_lst[i],borderColor=(0,255,0))

					camera_img_ = cv2.resize(img_lst[i], (0,0), fx=4, fy=4)					

					for i_ in rlen(markers):
						
						xy_ = 4 * markers[i_].corners_xy[0].mean(axis=0)
						#xy_ += np.array([cy_-10,cx_-10])
						
						xy_=tuple(xy_.astype(np.int))
						
						num_ = markers[i_].marker_id

						cv2.putText(
							camera_img_,
							d2n(markers[i_].marker_id),#num_),
							xy_,
							cv2.FONT_HERSHEY_SIMPLEX,
							0.75,(0,255,0),2) 
					k = mci(camera_img_,delay=33,scale=1)
					if k == ord('v'):
						while k != ord('b'):
							k = mci(camera_img_,delay=33,scale=1)
					elif k == ord('q'):
						print('quit')
						return None
				except Exception as e:
					print("********** Exception 123 ***********************")
					print(e.message, e.args)
				timer.message(d2s(i,'views =',views,int(100*i/(1.0*n)),'%'),color='white')
				#raw_enter()
		Frame_data = F
		return Frame_data

	F = get_Frame_data(D[left_image][vals])#+list(D[right_image][vals]))


