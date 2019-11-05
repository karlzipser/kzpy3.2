





#################
roscore &


python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 0 --step 0 --initial_index 25000

rosplay_menu.py


#python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019__/nodes --dic P
python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019_rgb_v1/nodes --dic P
# 8,12,-1,8,10

#python kzpy3/Cars/j26June2019__/nodes/network_node.py desktop_mode 1
python kzpy3/Cars/j26June2019_rgb_v1/nodes/network_node.py desktop_mode 1

python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py

python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__5April2019_2__18April2019_for_speed --dic P

#,b








#EOF
