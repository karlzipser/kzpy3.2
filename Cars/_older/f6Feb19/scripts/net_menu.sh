#!/bin/bash
OPTIONS='exit epoch6goodnet.SqueezeNet net_17Sep17_17h21m35s.SqueezeNet '
COLUMNS=12
echo 'network menu:'
select opt in $OPTIONS; do
	COLUMNS=12
	if [ "$opt" = 'epoch6goodnet.SqueezeNet' ]; then
		echo /home/nvidia/pytorch_models/epoch6goodnet.SqueezeNet
		rostopic pub -1 /bair_car/network_weights_name std_msgs/String /media/nvidia/rosbags/pytorch_models/epoch6goodnet.SqueezeNet
	elif [ "$opt" = 'net_17Sep17_17h21m35s.SqueezeNet' ]; then
		echo /home/nvidia/pytorch_models/net_17Sep17_17h21m35s.SqueezeNet
		rostopic pub -1 /bair_car/network_weights_name std_msgs/String /media/nvidia/rosbags/pytorch_models/net_17Sep17_17h21m35s.SqueezeNet
	elif [ "$opt" = 'exit' ]; then
	break
	else
		echo bad option
	fi
done
