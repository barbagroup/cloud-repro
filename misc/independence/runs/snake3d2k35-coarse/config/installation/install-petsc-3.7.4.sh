#!/bin/bash
# install PETSc-3.7.4

cd /tmp
PETSC_VERSION=3.7.4
wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-lite-${PETSC_VERSION}.tar.gz
PETSC_DIR=/opt/petsc/${PETSC_VERSION}
mkdir -p ${PETSC_DIR}
tar -xzf /tmp/petsc-lite-${PETSC_VERSION}.tar.gz -C ${PETSC_DIR} --strip-components=1
cd ${PETSC_DIR}
PETSC_ARCH=linux-gnu-opt
./configure --PETSC_DIR=${PETSC_DIR} --PETSC_ARCH=${PETSC_ARCH} \
	--with-mpi-dir=/usr/local \
        --COPTFLAGS="-O3" \
        --CXXOPTFLAGS="-O3" \
        --FOPTFLAGS="-O3" \
        --with-debugging=0 \
        --download-fblaslapack \
        --download-hypre \
        --download-hdf5 \
        --download-ptscotch \
        --download-metis \
        --download-parmetis \
        --download-superlu_dist
make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} all
make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} test
rm -f /tmp/petsc-lite-${PETSC_VERSION}.tar.gz
