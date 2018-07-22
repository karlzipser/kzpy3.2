#!/bin/bash
OPTIONS='exit a.SqueezeNet c.SqueezeNet d.SqueezeNet b.SqueezeNet b.SqueezeNet '
COLUMNS=12
echo 'network menu:'
select opt in $OPTIONS; do
	COLUMNS=12
	if [ "$opt" = 'a.SqueezeNet' ]; then
		echo /Users/karlzipser/Desktop/home/a.SqueezeNet
    rostopic pub -1 /bair_car/behavioral_mode std_msgs/String adjusted_steer
	elif [ "$opt" = 'c.SqueezeNet' ]; then
		echo /Users/karlzipser/Desktop/home/c.SqueezeNet
	elif [ "$opt" = 'd.SqueezeNet' ]; then
		echo /Users/karlzipser/Desktop/home/d.SqueezeNet
	elif [ "$opt" = 'b.SqueezeNet' ]; then
		echo /Users/karlzipser/Desktop/disk/b.SqueezeNet
	elif [ "$opt" = 'b.SqueezeNet' ]; then
		echo /Users/karlzipser/Desktop/disk2/b.SqueezeNet
	elif [ "$opt" = 'exit' ]; then
	break
	else
		echo bad option
	fi
done
