#!/bin/bash
# Run PetIBM

export CUDA_VISIBLE_DEVICES=0,1,2,3
CUDA_DIR="/usr/local/cuda-6.5"
export PATH="${CUDA_DIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${CUDA_DIR}/lib64:${LD_LIBRARY_PATH}"
AMGX_DIR="/opt/amgx"
export LD_LIBRARY_PATH="${AMGX_DIR}/lib:${LD_LIBRARY_PATH}"
export LM_LICENSE_FILE="${AMGX_DIR}/amgx_trial.lic"

mpiexec -np 24 petibm3d \
	-log_view \
	-malloc_log \
	-memory_view \
	-options_left
