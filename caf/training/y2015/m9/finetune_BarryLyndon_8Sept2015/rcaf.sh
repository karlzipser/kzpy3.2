#!/bin/bash -l
#SBATCH -p cortex
###SBATCH --constraint=cortex_gtx
#SBATCH -w n0001.cortex0
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=4G

#cd /global/home/users/karlz/kzpy/kzcaf 
module load caffe ipython
ipython train_gpu.py 


echo 'sbatch done'

exit
