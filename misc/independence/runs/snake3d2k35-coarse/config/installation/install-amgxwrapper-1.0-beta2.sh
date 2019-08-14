#!/bin/bash

AMGXWRAPPER_VERSION="1.0-beta2"
AMGXWRAPPER_DIR="/opt/amgxwrapper/${AMGXWRAPPER_VERSION}"
TARBALL="v${AMGXWRAPPER_VERSION}.tar.gz"

mkdir -p ${AMGXWRAPPER_DIR}
cd /tmp
wget https://github.com/barbagroup/AmgXWrapper/archive/${TARBALL}
tar -xzf ${TARBALL} -C ${AMGXWRAPPER_DIR} --strip-components=1

AMGXWRAPPER_POISSON="${AMGXWRAPPER_DIR}/example/Poisson"
cd ${AMGXWRAPPER_POISSON}

export CC=mpicc
export CXX=mpicxx

export PETSC_DIR="/opt/petsc/3.7.4"
export PETSC_ARCH="linux-gnu-opt"

cmake . \
  -DCUDA_TOOLKIT_ROOT_DIR="/usr/local/cuda-6.5" \
  -DAMGX_DIR="/opt/amgx/examples" \
  -DPETSC_DIR="/opt/petsc/3.7.4"
cmake . \
  -DCUDA_TOOLKIT_ROOT_DIR="/usr/local/cuda-6.5" \
  -DAMGX_DIR="/opt/amgx" \
  -DPETSC_DIR="/opt/petsc/3.7.4"

make

rm -f /tmp/${TARBALL}
