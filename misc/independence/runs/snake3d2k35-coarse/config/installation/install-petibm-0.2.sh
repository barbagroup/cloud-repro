#!/bin/bash
# install PetIBM-0.2

cd /tmp
PETIBM_VERSION=0.2
PETIBM_DIR=/opt/petibm/${PETIBM_VERSION}
mkdir -p ${PETIBM_DIR}
wget https://github.com/barbagroup/PetIBM/archive/v${PETIBM_VERSION}.tar.gz
tar -xzf v${PETIBM_VERSION}.tar.gz -C ${PETIBM_DIR} --strip-components=1
cd ${PETIBM_DIR}
./configure --prefix=/usr/local \
	CXX=mpicxx \
        CXXFLAGS="-O3 -w -std=c++11" \
        --with-petsc-dir=/opt/petsc/3.7.4 \
        --with-petsc-arch=linux-gnu-opt \
        --with-cuda=/usr/local/cuda \
        --with-amgx=/opt/amgx
make -j4 clean all install
rm -f /tmp/v${PETIBM_VERSION}.tar.gz
