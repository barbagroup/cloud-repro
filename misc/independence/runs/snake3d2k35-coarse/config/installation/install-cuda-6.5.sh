#!/bin/bash
# install CUDA-6.5 toolkit

CUDA_REPO_PKG=cuda-repo-ubuntu1404_6.5-14_amd64.deb
wget -O /tmp/${CUDA_REPO_PKG} http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1404/x86_64/${CUDA_REPO_PKG}
dpkg -i /tmp/${CUDA_REPO_PKG}
rm -f /tmp/${CUDA_REPO_PKG}
apt-get update
apt-get install cuda-drivers
apt-get install cuda-6-5
export PATH="/usr/local/cuda-6.5/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-6.5/lib64:$LD_LIBRARY_PATH"
cd /usr/local/cuda-6.5/samples/1_Utilities/deviceQuery
make all
./deviceQuery
