#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
simudir=$scriptdir

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

# get number of nodes
IFS=',' read -ra HOSTS <<< "$AZ_BATCH_HOST_LIST"
nodes=${#HOSTS[@]}
echo "Number of nodes: $nodes"
echo "Hosts: $AZ_BATCH_HOST_LIST"
# number of processes per node
ppn=16
echo "Number of processes per node to use: $ppn"
# number of processes
np=$(($nodes * $ppn))
echo "Total number of processes: $np"

echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

cd $simudir

cp $AZ_BATCH_TASK_DIR/stdout.txt .
cp $AZ_BATCH_TASK_DIR/stderr.txt .

niters=5
counter=1

while [ $counter -le $niters ]
do
	echo "Run $counter" > stdout_run$counter.txt
	mpirun -np $np -ppn $ppn -host $AZ_BATCH_HOST_LIST \
		poisson \
		-caseName poisson_petsc_nodes$nodes_run$counter \
		-mode PETSc \
		-cfgFileName config/poisson_solver.info \
		-Nx 1000 -Ny 1000 -Nz 50 \
		-log_view ascii:view_run$counter.log \
		-options_left >> stdout_run$counter.txt 2> stderr_run$counter.txt
	((counter++))
done

rm -rf data

exit 0
