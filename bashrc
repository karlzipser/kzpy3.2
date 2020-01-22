#clear
#echo "Start kzpy3/bashrc..."

source ~/kzpy3/misc/auto_aliases

source ~/kzpy3/Menu/complete.sh
source ~/kzpy3/Learn/complete.sh

alias ls='ls -alh'
alias rlog='rm -r ~/.ros/log/*'
alias rla='rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=true' 
alias rlanz='rrm;rlog;rm ~/Desktop/Mr*.txt;roslaunch bair_car bair_car.launch use_zed:=false record:=true'
alias rlanznr='rrm;rlog;rm ~/Desktop/Mr*.txt;roslaunch bair_car bair_car.launch use_zed:=false record:=False'
alias rgy='rostopic echo /bair_car/gyro'
alias rgp='rostopic echo /bair_car/gps'
alias rac='rostopic echo /bair_car/acc'
alias rst='rostopic echo /bair_car/steer'
alias rmo='rostopic echo /bair_car/motor'
alias ren='rostopic echo /bair_car/encoder'

alias ssd='sudo shutdown -h now'
alias srb='sudo reboot'
alias rivl='rosrun image_view image_view image:=/bair_car/zed/left/image_rect_color'
alias rivr='rosrun image_view image_view image:=/bair_car/zed/right/image_rect_color'
alias rri='rosrun image_view image_view image:=/bair_car/os1_node/image'
alias zed_explorer='/usr/local/zed/tools/ZED\ Explorer'
alias pgacps='bash ~/kzpy3/scripts/connect/pgacpssh.sh'
alias fixScreen='DISPLAY=:0 xrandr --output HDMI-0 --mode 1024x768'

alias rosdo="sudo chmod -R 777 /media/$(whoami)/rosbags*"
alias rcd='cd /media/$(whoami)/rosbags'


alias kr='~/kzpy3/scripts/kill_ros.sh'
alias ssx='screen -S SX'
alias ssy='screen -S SY'
alias ssz='screen -S SZ'
alias ssa='screen -S SA'
alias ssb='screen -S SB'
alias ssc='screen -S SC'
alias srx='screen -r SX'
alias sry='screen -r SY'
alias srz='screen -r SZ'
alias sra='screen -r SA'
alias srb='screen -r SB'
alias src='screen -r SC'

alias Data='python ~/kzpy3/Data_app/Main.py'
alias pGraph='python ~/kzpy3/Grapher_app_for_preprocessed_data/Main.py'
alias rGraph='python ~/kzpy3/Grapher_app_for_live_ros_data/Main.py'

alias m="~/kzpy3/Menu/main.py"
alias n="~/kzpy3/Menu/main.py --path kzpy3/Menu/quick"
alias otn='kzpy3/scripts/connect/open_tab_with_quick_menu.sh'

alias gacp="git add .;git commit -m 'gacp';git push origin master"
alias pgacp='cd ~/kzpy3; git pull; gacp; cd'
alias pgp='cd ~/kzpy3; git pull; cd'
git config --global credential.helper "cache --timeout=86400"
alias ipy="ipython --no-banner"

export PYTHONPATH=~:$PYTHONPATH
export PYTHONPATH=~/kzpy3:$PYTHONPATH

if [ "$(whoami)" == "nvidia" ]
  then
    sudo bash ~/kzpy3/scripts/gen/clean_pycs.sh ~/kzpy3
    export PYTHONSTARTUP=~/kzpy3/utils3.py
  else
    export PYTHONSTARTUP=~/kzpy3/vis3.py
    bash ~/kzpy3/scripts/gen/clean_pycs.sh ~/kzpy3
fi

export PATH=~/kzpy3:$PATH
export PATH=~/kzpy3/scripts:$PATH
export PATH=~/kzpy3/scripts/connect:$PATH
export PATH=~/kzpy3/scripts/gen:$PATH
export PATH=~/kzpy3/scripts/net:$PATH
export PATH=~/kzpy3/scripts/osx:$PATH
export PATH=~/kzpy3/scripts/ros:$PATH
export PATH=~/kzpy3/Commands:$PATH
export PATH=~/kzpy3/misc:$PATH
export PATH=~/kzpy3/Menu:$PATH

alias sb='cd;source ~/.bashrc'
#######################################################
#
export COMPUTER_NAME=$HOSTNAME #'' #
#PS1="$COMPUTER_NAME\W $ "
PS1="\[\033[01;35m\]\w\[\033[00m\] $ "
if [ $HOSTNAME == "bdd2" ]
  then
    PS1="\[\033[01;32m\]$HOSTNAME\w\[\033[00m\] $ "
fi
if [ $HOSTNAME == "bdd4" ]
  then
    PS1="\[\033[01;32m\]***$HOSTNAME***\w\[\033[00m\] $ "
fi
if [ "$(whoami)" == "nvidia" ]
  then
    export COMPUTER_NAME=$HOSTNAME
    PS1="$COMPUTER_NAME> \W $ "
    source /opt/ros/kinetic/setup.bash
    source ~/catkin_ws/devel/setup.bash
fi
#
#######################################################

alias rzl='show_image_from_ros.py --scale 2 --topic /bair_car/zed/left/image_rect_color'
alias rzr='show_image_from_ros.py --scale 2 --topic /bair_car/zed/right/image_rect_color'
alias rou='show_image_from_ros.py --scale --2 topic /os1_node/image'

alias menu='python ~/kzpy3/Menu/main.py'


#python kzpy3/scripts/connect/quick_print.py

#date
#echo "...End kzpy3/bashrc"
#if [ "$(whoami)" == "nvidia" ]
#  then
#    n
#  else
#    echo 'done.'
    #echo 'ssh in 2'
    #sleep 2
    #qssh.py
#fi

if [ "$(whoami)" != "nvidia" ]
  then
    export HISTSIZE=2000
    export HISTFILESIZE=4000
fi

alias U3='ssh -p 1022 -XY karlzipser@169.229.219.141'
alias U='ssh -p 1022 -XY karlzipser@169.229.219.140'

#EOF
