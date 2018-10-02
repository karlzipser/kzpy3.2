rm ~/Desktop/bw.txt
rostopic bw /bair_car/zed/left/image_rect_color > ~/Desktop/bw.txt &
sleep 3
killall rostopic
mv ~/Desktop/bw.txt ~/Desktop/left_image_rect_color_bw.txt
rm ~/Desktop/bw.txt