#!/bin/bash
# install OpenMPI-1.8.8

cd /tmp
OPENMPI_VERSION=1.8.8
wget https://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-${OPENMPI_VERSION}.tar.gz
OPENMPI_DIR=/opt/openmpi/${OPENMPI_VERSION}
mkdir -p ${OPENMPI_DIR}
tar -xzf /tmp/openmpi-${OPENMPI_VERSION}.tar.gz -C ${OPENMPI_DIR} --strip-components=1
cd ${OPENMPI_DIR}
./configure --prefix=/usr/local \
	CC=gcc-5 \
        CFLAGS="-O3" \
        CXX=g++-5 \
        CXXFLAGS="-O3" \
        FC=gfortran-5 \
        FCFLAGS="-O3"
make -j"$(nproc)" install
ldconfig /usr/local/lib
rm -f /tmp/openmpi-${OPENMPI_VERSION}.tar.gz
