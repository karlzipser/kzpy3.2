clear

alias ls='ls -al'
alias rhz='rostopic hz /bair_car/zed/left/image_rect_color'
alias rls='ls -al /media/nvidia/rosbags'
alias rrm='rm ~/catkin_ws/src/bair_car/rosbags/*'
alias rlog='rm -r ~/.ros/log/*'
alias rla='rrm;rlog;rm ~/Desktop/Mr*.txt;roslaunch bair_car bair_car.launch use_zed:=true record:=true' 
alias rlanz='rrm;rlog;rm ~/Desktop/Mr*.txt;roslaunch bair_car bair_car.launch use_zed:=false record:=true' 
alias rgy='rostopic echo /bair_car/gyro'
alias rgp='rostopic echo /bair_car/gps'
alias rac='rostopic echo /bair_car/acc'
alias rst='rostopic echo /bair_car/steer'
alias rmo='rostopic echo /bair_car/motor'
alias ren='rostopic echo /bair_car/encoder'
alias rcd='cd /media/nvidia/rosbags'
alias ssd='sudo shutdown -h now'
alias srb='sudo reboot'
alias rcn='echo $COMPUTER_NAME'
alias rivl='rosrun image_view image_view image:=/bair_car/zed/left/image_rect_color'
alias rivr='rosrun image_view image_view image:=/bair_car/zed/right/image_rect_color'
alias zed_explorer='/usr/local/zed/tools/ZED\ Explorer'

alias fixScreen='DISPLAY=:0 xrandr --output HDMI-0 --mode 1024x768'

alias kx='killall xterm'
alias rosdo="sudo chmod -R 777 /media/$(whoami)/rosbags*"

alias ssx='screen -S SX'
alias ssy='screen -S SY'
alias ssz='screen -S SZ'
alias srx='screen -r SX'
alias sry='screen -r SY'
alias srz='screen -r SZ'

alias Data='python ~/kzpy3/Data_app/Main.py'
alias pGraph='python ~/kzpy3/Grapher_app_for_preprocessed_data/Main.py'
alias rGraph='python ~/kzpy3/Grapher_app_for_live_ros_data/Main.py'
alias Train='ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_31May3018/Main.py'
alias Localization='python ~/kzpy3/Localization_app/Main.py'

######################## for .bashrc from MacBook #################
#
alias gacp="git add .;git commit -m 'gacp';git push origin master"
alias pgacp='cd ~/kzpy3; git pull; gacp; cd'
alias pgp='cd ~/kzpy3; git pull; cd'
git config --global credential.helper "cache --timeout=86400"
alias ipy="ipython --no-banner"
alias td2="mv ~/Desktop/* ~/Desktop2/"

export PYTHONPATH=~:$PYTHONPATH
export PYTHONSTARTUP=~/kzpy3/utils2.py
export PATH=~/kzpy3/scripts:$PATH
export PATH=~/kzpy3/scratch:$PATH
export PATH=~/kzpy3/misc:$PATH



alias sb='cd;source ~/.bashrc'

#######################################################
#
if [ "$(whoami)" == "nvidia" ]
then



export COMPUTER_NAME=$HOSTNAME
PS1="$COMPUTER_NAME> \W $ "
source /opt/ros/kinetic/setup.bash
source ~/catkin_ws/devel/setup.bash
export PYTHONPATH=~:$PYTHONPATH
export PYTHONPATH=~/kzpy3:$PYTHONPATH
export PATH=~/kzpy3/utils:$PATH
export PATH=~/kzpy3:$PATH
#export PARAMIKO_TARGET_IP='192.168.1.103'
#export RECEIVE_STEER_MOTOR_FROM_PARAMIKO='True'


#sudo rm /etc/hosts
#rm ~/hosts
make_hosts.py &
#sudo ln -s ~/hosts /etc/hosts



echo Hi $COMPUTER_NAME on Jetson
echo "rrm;rlog"
rrm
rlog
OPTIONS="exit screen rla rlanz rosbags git_pull reboot shutdown rostopics arduino_node_menu network_node_menu df car_link_menu"
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
   elif [ "$opt" = "rlanz" ]; then
    rlanz
   elif [ "$opt" = "rla" ]; then
    rrm;rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=true
   elif [ "$opt" = "car_link_menu" ]; then
    ~/kzpy3/Cars/car_link_menu.sh
    elif [ "$opt" = "net_menu" ]; then
      bash ~/kzpy3/Cars/car_16July2018_stable/scripts/net_menu.sh
   elif [ "$opt" = "rosbags" ]; then
    check_rosbags.py
   elif [ "$opt" = "rostopics" ]; then
    python ~/catkin_ws/src/bair_car/scripts/rostopics.py
   elif [ "$opt" = "arduino_node_menu" ]; then
    python ~/kzpy3/Menu_app/node_menu.py NODE arduino
   elif [ "$opt" = "network_node_menu" ]; then
    python ~/kzpy3/Menu_app/node_menu.py NODE network
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
#
#######################################################

date




#EOF
