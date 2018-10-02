rm ~/Desktop/os1_node_points_bw.txt
rostopic bw /os1_node/points > ~/Desktop/os1_node_points_bw.txt &
sleep 3
killall rostopic
sleep 1
more ~/Desktop/os1_node_points_bw.txt














