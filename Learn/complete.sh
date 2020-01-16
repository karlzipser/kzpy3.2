#!/usr/bin/env bash
complete -o default -W "--LR --GPU ConDecon_test2 --backwards False --momentum ConDecon_Fire --losses_to_average --resume --type --runs --default-- train XOR ConDecon_Fire_FS --save_timer_time validate Runs_Values True --Help --batch_size" Learn
