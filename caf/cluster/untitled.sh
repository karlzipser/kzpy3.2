#!/bin/sh
module load cmake
module load gcc atlas hdf5/1.8.11-gcc-s
module load python/2.7.8 numpy/1.9.0 scikit-image/0.10.1 boost/1.54.0-python-2.7.8
module load matlab/R2013a
module load cuda/6.5
module load protobuf glog gflags leveldb lmdb opencv snappy
make clean
make -j8 all 2>&1 | tee caffe.make.log
make -j8 pycaffe 2>&1 | tee -a caffe.make.log
make -j8 matcaffe 2>&1 | tee -a caffe.make.log
make -j8 test 2>&1 | tee caffe.test.log
make runtest 2>&1 | tee caffe.runtest.log