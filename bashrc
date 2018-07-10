clear

alias ls='ls -al'
alias rhz='rostopic hz /bair_car/zed/left/image_rect_color'
alias rls='ls -al /media/nvidia/rosbags'
alias rrm='rm ~/catkin_ws/src/bair_car/rosbags/*'
alias rlog='rm -r ~/.ros/log/*'
alias rla='rrm;rlog;rm ~/Desktop/Mr*.txt;roslaunch bair_car bair_car.launch use_zed:=true record:=true' 
alias rlanr='rrm;rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=false' 
alias rlab='(rla 3>&1 1>&2 2>&3 | grep -v "slMat2cvMat: mat type currently not supported 0 0") 3>&1 1>&2 2>&3'
alias rgy='rostopic echo /bair_car/gyro'
alias rgp='rostopic echo /bair_car/gps'
alias rac='rostopic echo /bair_car/acc'
alias rst='rostopic echo /bair_car/steer'
alias rmo='rostopic echo /bair_car/motor'
alias ren='rostopic echo /bair_car/encoder'
alias rcd='cd /media/nvidia/rosbags'
alias ssd='sudo shutdown -h now'
alias srb='sudo reboot'
alias killros='killall python && killall roslaunch && killall record'
alias rcn='echo $COMPUTER_NAME'
alias rivl='rosrun image_view image_view image:=/bair_car/zed/left/image_rect_color'
alias rivr='rosrun image_view image_view image:=/bair_car/zed/right/image_rect_color'
alias rlat='rostopic echo /bair_car/GPS2_lat'
alias rstat='python ~/kzpy3/teg_older/teg7/data/rosstatus.py'
alias test_caffe='cd ~/caffe; build/tools/caffe time --model=models/bvlc_alexnet/deploy.prototxt --gpu=0'
alias zed_explorer='/usr/local/zed/tools/ZED\ Explorer'
alias sopen="open -a /Applications/Sublime\ Text\ 2.app/"

alias fixScreen='DISPLAY=:0 xrandr --output HDMI-0 --mode 1024x768'

alias Mr_Blue='ssh nvidia@192.168.1.101'
alias Mr_Black='ssh nvidia@192.168.1.102'
alias Mr_Orange='ssh nvidia@192.168.1.103'
alias Mr_Yellow='ssh nvidia@192.168.1.104'
alias Mr_Lt_Blue='ssh nvidia@192.168.1.105'
alias Mr_Purple='ssh nvidia@192.168.1.106'
alias Mr_TX2='ssh nvidia@192.168.1.201'
alias Mr_Forward192='ssh nvidia@192.168.1.107'
alias Mr_Forward10='ssh nvidia@10.0.0.107'
alias Mr_Back192='ssh nvidia@192.168.1.201'
alias Mr_Back10='ssh nvidia@10.0.0.201'

alias bu='Mr_Blue'
alias bk='Mr_Black'
alias or='Mr_Orange'
alias ye='Mr_Yellow'
alias lt='Mr_Lt_Blue'
alias pu='Mr_Purple'
alias tx='Mr_TX2'

alias kx='killall xterm'
alias rosdo='sudo chmod -R 777 /media/karlzipser/rosbags*'
######################## for .bashrc from MacBook #################
#
#export DISPLAY=:0.0
alias gacp="git add .;git commit -m 'gacp';git push origin master"
alias pgacp='cd ~/kzpy3; git pull; gacp; cd'
#alias gp3="~/kzpy3/kzpy3_git_pull.sh"
#alias gckzpy3="git clone https://github.com/karlzipser/kzpy3.0.git"
git config --global credential.helper "cache --timeout=86400"
alias ipy="ipython --no-banner"
export PYTHONPATH=~:$PYTHONPATH
export PYTHONSTARTUP=~/kzpy3/vis2.py
export PATH=~/kzpy3/scripts:$PATH
export PATH=~/caffe/build/tools:$PATH
export PYTHONPATH=~/caffe/python:$PYTHONPATH
export PYTHONPATH=~/kzpy3/Sascha/data_analysis_14April2017:$PYTHONPATH
export PATH=~/kzpy3/c:$PATH

alias Grapher='python ~/kzpy3/Grapher_app/Main.py'
alias Grapher3='python ~/kzpy3/Grapher_app_3rd_pass/Main.py'
alias Car_Data='python ~/kzpy3/Car_Data_app/Main.py'
alias Train='python ~/kzpy3/Train_app/Main.py'
alias Localization='python ~/kzpy3/Localization_app/Main.py'

if [ "$(whoami)" == "nvidia" ]
then
echo Hi $COMPUTER_NAME on Jetson
#export ROS_IP=0.0.0.0 # Listen on any interface
#echo "cd ~/kzpy3;git pull;cd"
#cd ~/kzpy3
#git pull
#cd
echo "rrm;rlog"
rrm
rlog
alias sb='cd;source ~/.bashrc'
OPTIONS="exit screen rla rlanr rosbags git_pull reboot shutdown df car_link_menu"
COLUMNS=12
echo 'main menu'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "reboot" ]; then
    echo "Rebooting . . ."
    sudo reboot
   elif [ "$opt" = "shutdown" ]; then
    echo "Shutting down . . ."
    ssd
   elif [ "$opt" = "rlanr" ]; then
    rrm;rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=false car_name:=$COMPUTER_NAME
   elif [ "$opt" = "rla" ]; then
    rrm;rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=true
   elif [ "$opt" = "car_link_menu" ]; then
    ~/kzpy3/Cars/car_link_menu.sh
   elif [ "$opt" = "rosbags" ]; then
    check_rosbags.py
   elif [ "$opt" = "git_pull" ]; then
    cd ~/kzpy3
    git pull
    cd
   elif [ "$opt" = "screen" ]; then
    screen 
   elif [ "$opt" = "exit" ]; then
    break 
   elif [ "$opt" = "df" ]; then
    df 
   else
    #clear
    echo bad option
   fi
done
fi

date


# chmod -R 744 xyz