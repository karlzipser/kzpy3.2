clear
echo "Start kzpy3/bashrc..."
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
alias rply='python ~/kzpy3/scripts/rosplay_menu.py'
alias fixScreen='DISPLAY=:0 xrandr --output HDMI-0 --mode 1024x768'

alias kx='killall xterm'
alias rosdo="sudo chmod -R 777 /media/$(whoami)/rosbags*"

alias ssx='screen -S SX'
alias ssy='screen -S SY'
alias ssz='screen -S SZ'
alias ssa='screen -S SA'
alias ssb='screen -S SB'
alias ssc='screen -S SC'
#alias ssd='screen -S SD'
alias srx='screen -r SX'
alias sry='screen -r SY'
alias srz='screen -r SZ'
alias sra='screen -r SA'
alias srb='screen -r SB'
alias src='screen -r SC'
#alias srd='screen -r SD'

alias Data='python ~/kzpy3/Data_app/Main.py'
alias pGraph='python ~/kzpy3/Grapher_app_for_preprocessed_data/Main.py'
alias rGraph='python ~/kzpy3/Grapher_app_for_live_ros_data/Main.py'
alias Train='ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_31May3018/Main.py'
alias Train_='ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_31May3018_temp_sequential/Main.py'
alias Train40='ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_15Sept2018/Main.py'

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
#export PYTHONSTARTUP=~/kzpy3/utils.py
export PYTHONSTARTUP=~/kzpy3/utils3.py
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
    #export PYTHONPATH=~:$PYTHONPATH
    export PYTHONPATH=~/kzpy3:$PYTHONPATH
    export PATH=~/kzpy3/utils:$PATH
    export PATH=~/kzpy3:$PATH

    #sudo rm /etc/hosts
    #rm ~/hosts
    #make_hosts.py &
    echo "Not running make_hosts.py"
    #sudo ln -s ~/hosts /etc/hosts
fi
#
#######################################################

date


export ccar='kzpy3/Cars/car_24July2018/nodes'
export ctrain='kzpy3/Train_app'
export cmenu='kzpy3/Menu_app'
export cdata='kzpy3/Data_app'
export PYTHONPATH=~/kzpy3:$PYTHONPATH

echo "...End kzpy3/bashrc"
#EOF
