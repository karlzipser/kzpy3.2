#!/bin/sh
# Some of the instructions taken from https://github.com/jetsonhacks/installCaffeJTX1

sudo add-apt-repository universe
sudo apt-get update -y

# Install git
sudo apt-get install -y git

/bin/echo -e "\e[1;32mLoading Caffe Dependencies.\e[0m"
sudo apt-get install cmake -y
# General Dependencies
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev \
libhdf5-serial-dev protobuf-compiler -y
sudo apt-get install --no-install-recommends libboost-all-dev -y
# BLAS
sudo apt-get install libatlas-base-dev -y
# Remaining Dependencies
sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev -y

# added for numpy support
#sudo pip install numpy
sudo apt-get install -y python-numpy

sudo usermod -a -G video $USER
/bin/echo -e "\e[1;32mCloning Caffe into the home directory\e[0m"
# Place caffe in the home directory
cd ~/
# Git clone Caffe
git clone https://github.com/BVLC/caffe.git
cd caffe 

#Additional 
sudo apt-get install -y python-pip
sudo pip install scipy # required by scikit-image
sudo apt-get install -y python-scipy # in case pip failed

cd python
for req in $(cat requirements.txt); do sudo pip install $req; done
echo "export PYTHONPATH=$(pwd):$PYTHONPATH " >> ~/.bashrc # to be able to call "import caffe" from Python after reboot
source ~/.bashrc # Update shell 
sudo ldconfig
cd ..

cp Makefile.config.example Makefile.config
# Enable cuDNN usage
sudo sed -i 's/# USE_CUDNN := 1/USE_CUDNN := 1/' Makefile.config
# Enable with python layer
sudo sed -i 's/# WITH_PYTHON_LAYER := 1/WITH_PYTHON_LAYER := 1/' Makefile.config

mkdir build
cd build
cmake ..
cd ..

make pycaffe -j3
make all -j3
# make test -j3
make runtest -j3
make distribute

# Caffe Web_demo
sudo pip install -r examples/web_demo/requirements.txt
# Reference CaffeNet Model and the ImageNet Auxiliary Data
./scripts/download_model_binary.py models/bvlc_reference_caffenet
./data/ilsvrc12/get_ilsvrc_aux.sh
#Reference CaffeNet Model and the ImageNet Auxiliary Data

# NGINX
sudo apt-get install -y nginx
sudo /etc/init.d/nginx start
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/web_demo
sudo ln -s /etc/nginx/sites-available/web_demo /etc/nginx/sites-enabled/web_demo
echo ' 
server {
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias  /home/www/flask_project/static/;
    }
}' | sudo tee -a /etc/nginx/sites-available/web_demo
sudo /etc/init.d/nginx restart

source ~/.bashrc # Update shell 
sudo ldconfig
