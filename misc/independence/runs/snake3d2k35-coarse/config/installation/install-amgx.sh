#!/bin/bash
# setup AmgX

AMGX_DIR=/opt/amgx
mkdir -p ${AMGX_DIR}
unzip 2014.12.22_amgx_redhat-6.5_cuda-6.5_openmpi-1.7.2.zip -d ${AMGX_DIR}
cp "amgx_trial.lic" ${AMGX_DIR}
