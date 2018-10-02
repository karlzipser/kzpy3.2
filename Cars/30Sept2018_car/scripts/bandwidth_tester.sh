rm ~/Desktop/bw.txt
rostopic bw /bair_car/zed/left/image_rect_color > ~/Desktop/bw.txt &
sleep 3
killall rostopic
mv bw.txt left_image_rect_color_bw.txt