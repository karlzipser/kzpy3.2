rm ~/Desktop/os1_node_points_bw.txt
rostopic bw /os1_node/points > ~/Desktop/os1_node_points_bw.txt &
sleep 3
killall rostopic


rm ~/Desktop/left_image_rect_color_bw.txt
rostopic bw /bair_car/zed/left/image_rect_color > ~/Desktop/left_image_rect_color_bw.txt &
sleep 3
killall rostopic














