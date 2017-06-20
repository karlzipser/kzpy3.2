from kzpy3.vis import *
import rospy
import rosbag
import cv2
from cv_bridge import CvBridge,CvBridgeError
import threading
import kzpy3.teg9.data.animate as animate
import kzpy3.teg9.data.utils.raw_marker_data_to_cubic_splines as raw_marker_data_to_cubic_splines
if '__file__' not in vars():
    __file__ = "__file__ NOT DEFINED"


bridge = CvBridge()

image_topics = ['left_image','right_image']
camera_sides = ['left','right']





def multi_process_bag_folders(bag_folders_path_lst,meta_path,visualize=0):
    print bag_folders_path_lst
    for pl in bag_folders_path_lst:
        print pl
        bag_folders = sgg(opj(pl,'*'))
        try:
            for bf in bag_folders:
                print bf
                multi_preprocess_bagfiles(bf,meta_path,visualize)
        except Exception as e:
            print("********** Exception ***********************")
            print(e.message, e.args)






def multi_preprocess_bagfiles(bag_folder_path,meta_path,visualize=0):
    print bag_folder_path
    bag_files = sgg(opj(bag_folder_path,'*.bag'))
    run_name = fname(pname(bag_files[0]))
    if len(gg(opj(meta_path,run_name))) == 0:
        print("Making "+opj(meta_path,run_name))
        unix('mkdir -p '+opj(meta_path,run_name))
    if len(gg(opj(meta_path,run_name,'marker_data.pkl'))) == 1:
        print(opj(meta_path,run_name,'marker_data.pkl')+' exists, doing nothing.')
        return
    A = {}
    A['bag_folder_path'] = bag_folder_path
    for s in ['left','right']:
        A[s] = {}

    for path in bag_files:
        print('############## '+path+' #############')
        try:
           preprocess_bagfiles(A,path,visualize)
        except Exception as e:
            print("********** Exception ***********************")
            print(e.message, e.args)
    save_obj(A,opj(meta_path,run_name,'marker_data.pkl'))






def preprocess_bagfiles(A,path,visualize):
    from kzpy3.data_analysis.Angle_Dict_Creator import get_angles_and_distance
    ctr = 0
    timer = Timer(0)
    
    cprint('Loading bagfile '+path,'yellow')

    bag = rosbag.Bag(path)

    color_mode = "rgb8"
    for s in ['left','right']:
        for m in bag.read_messages(topics=['/bair_car/zed/'+s+'/image_rect_color']):
            t = round(m.timestamp.to_time(),3)
            A[s][t] = {}
            img = bridge.imgmsg_to_cv2(m[1],color_mode)
            angles_to_center, angles_surfaces, distances_marker, markers = get_angles_and_distance(img)
            A[s][t]['angles_to_center'] = angles_to_center
            A[s][t]['angles_surfaces'] = angles_surfaces
            A[s][t]['distances_marker'] = distances_marker
            A[s][t]['markers'] = markers
            
            if visualize > 0:
                if np.mod(ctr,visualize) == 0:
                    print(d2c(fname(path),s,t,A[s][t]['distances_marker']))
                    k = mci(img)
                    if k == ord('q'):
                        break
                ctr += 1
    print(d2s('Done in',timer.time(),'seconds'))






meta_path = '/home/karlzipser/Desktop/bair_car_data_new/meta'

Mr_Black = ['/media/karlzipser/ExtraDrive1/Mr_Black_25April2017/processed', 
            '/media/karlzipser/ExtraDrive1/Mr_Black_28April2017/processed', 
            '/media/karlzipser/ExtraDrive1/Mr_Black_30April2017/processed'
            ]

Mr_Orange = ['/media/karlzipser/ExtraDrive2/Mr_Orange_25April2017/processed', 
            '/media/karlzipser/ExtraDrive2/Mr_Orange_28April2017/processed', 
            '/media/karlzipser/ExtraDrive2/Mr_Orange_30April2017/processed'
            ]

Mr_Blue = ['/media/karlzipser/ExtraDrive3/Mr_Blue_25April2017/processed', 
            '/media/karlzipser/ExtraDrive3/Mr_Blue_28April2017/processed', 
            '/media/karlzipser/ExtraDrive3/Mr_Blue_30April2017/processed'
            ]

Mr_Yellow_Silver = ['/media/karlzipser/ExtraDrive4/Mr_Yellow_25April2017/processed', 
            '/media/karlzipser/ExtraDrive4/Mr_Yellow_28April2017/processed', 
            '/media/karlzipser/ExtraDrive4/Mr_Yellow_30April2017/processed',
            '/media/karlzipser/ExtraDrive4/Mr_Silver_28April2017/processed']


Mr_Mixed =['/media/karlzipser/ExtraDrive3/from_Mr_Yellow/Mr_Yellow_Fern_11April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Yellow/Mr_Yellow_Fern_14April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Yellow/Mr_Yellow_Fern_15April2017/new',
'/media/karlzipser/ExtraDrive3/from_Mr_Silver/Mr_Silver_Fern_11April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Orange/Mr_Orange_11_13April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Blue/Mr_Blue_Fern_15April2017/new',
'/media/karlzipser/ExtraDrive3/from_Mr_Blue/Mr_Blue_Fern_14April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Blue/Mr_Blue_Fern_11April2017/processed',
'/media/karlzipser/ExtraDrive3/from_Mr_Black/Mr_Black_Fern_15April2017/new' 
]




if False:
    CS_("Get raw marker data from bag file images to pkl files.",fname(__file__))
    multi_process_bag_folders(Mr_Mixed,meta_path,100)



if False:
    CS_("Process marker_data.pkl files to get cubic spline trajectories.",fname(__file__))
    bag_folders_path = opjD('bair_car_data_new')
    bag_folders_meta_path = opj(bag_folders_path,'meta')
    aruco_runs = []
    marker_data_files = sggo(bag_folders_meta_path,'*','marker_data.pkl')
    for m in marker_data_files:
        aruco_runs.append(fname(pname(m)))
    M = {}
    for a in aruco_runs:
        raw_marker_data_to_cubic_splines.process_run_data(a,bag_folders_meta_path,M)
        car_name = raw_marker_data_to_cubic_splines.car_name_from_run_name(a)
        cprint(M[car_name][a].keys(),'yellow')
        so(opj(bag_folders_meta_path,a,'trajectory.pkl'),M[car_name][a])
        #unix('rm '+opj(bag_folders_meta_path,a,'cubic_splines.pkl'))

if True:
    import kzpy3.teg9.data.utils.get_trajectory_points as get_trajectory_points

    CS_("Process trajectory.pkl files.",fname(__file__))
    bag_folders_path = opjD('bair_car_data_new')
    bag_folders_meta_path = opj(bag_folders_path,'meta')
    aruco_runs = []
    trajectory_files = sggo(bag_folders_meta_path,'*','trajectory.pkl')
    for m in trajectory_files:
        aruco_runs.append(fname(pname(m)))
    M = {}


    for run_name in aruco_runs:
        car_name = get_trajectory_points.car_name_from_run_name(run_name)
        if car_name not in M:
            M[car_name] = {}
        M[car_name][run_name] = lo(opj(bag_folders_meta_path,run_name,'trajectory.pkl'))
        print('loaded '+car_name+' '+run_name)

        
    CS_("""
    choose a run
    assert less than two hours long
    find all other runs that are overlapping in time
    sample all cubic splines with timestamps of given run.
    save all timestamp synched splines in given run's meta folder
    """)

heights = {'Mr_Yellow':1, 'Mr_Silver':2, 'Mr_Blue':3, 'Mr_Orange':4, 'Mr_Black':5}
Origin = 300
Mult = 50
dt = 1/30.0



for ref_run_name in aruco_runs:

    for side in ['left']:
        clf()
        car_name = get_trajectory_points.car_name_from_run_name(ref_run_name)
        R = M[car_name][ref_run_name][side]['raw_time_stamps']
        R0,Rn = R[0],R[-1]
        M[car_name][ref_run_name]['self_trajectory'] = get_trajectory_points.get_xp_pts(M,ref_run_name,R,Mult,Origin,dt)
        M[car_name][ref_run_name]['other_trajectories'] = []
        ref_car_name = car_name
        plot([R[0],R[-1]],[heights[car_name],heights[car_name]],marker='.',linestyle='--',color='r')
        title(ref_run_name)
    cases = []
    for car_name in M.keys():
        for run_name in M[car_name]:
            if run_name != ref_run_name:
                for side in ['left']:
                    T = M[car_name][run_name][side]['time_stamps']
                    t0,tn = T[0],T[-1]
                    case = False
                    if (R0<t0 and Rn>t0):
                        case = 1
                    elif (R0<tn and Rn>tn):
                        case = 2
                    elif (R0>t0 and Rn<tn):
                        case = 3
                    if case:
                        cases.append(case)
                        plot([T[0],T[-1]],[heights[car_name],heights[car_name]],marker='.',linestyle='--',color='b')
                        other_trajectories_modified_timestamps = []
                        for r in R:
                            if r >= t0 and r <= Rn:
                                other_trajectories_modified_timestamps.append(r)
                        traj = get_trajectory_points.get_xp_pts(M,run_name,other_trajectories_modified_timestamps,Mult,Origin,dt)
                        M[ref_car_name][ref_run_name]['other_trajectories'].append(traj)
            else:
                print('found ref run')
    print cases
    ylim(0.5,5.5)
    pause(0.001)
   # raw_input('?')

N = {}
for car_name in M.keys():
    N[car_name] = {}
    for run_name in M[car_name]:
        N[car_name][run_name] = {}
        N[car_name][run_name]['self_trajectory'] = M[car_name][run_name]['self_trajectory']
        N[car_name][run_name]['other_trajectories'] = M[car_name][run_name]['other_trajectories']
so(N,opjD('N.pkl'))

