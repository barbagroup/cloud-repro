#!/usr/bin/env bash

#SBATCH --job-name="osu"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=ivygpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:20:00

source /c1/apps/intel-cluster-studio/2017.4/compilers_and_libraries_2017.4.196/linux/mpi/intel64/bin/mpivars.sh

bindir="/groups/barbalab/software/osu-micro-benchmarks/5.6-intelmpi/mpi/pt2pt"
export PATH=$bindir:$PATH

# number of runs
nruns=5

outdir="/home/mesnardo/runs/osubenchmarks/colonialone-intelmpi/output"
mkdir -p $outdir
cd $outdir

for i in `seq 1 5`; do
	mpirun -n 2 --ppn 1 \
		-env I_MPI_FABRICS=dapl \
		-env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 \
		-env I_MPI_DYNAMIC_CONNECTION=0 \
		osu_latency \
		-x 100 -i 10000 H H \
		>> $outdir/stdout_latency_run$i.txt 2> $outdir/stderr_latency_run$i.txt

	mpirun -n 2 --ppn 1 \
		-env I_MPI_FABRICS=dapl \
		-env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 \
		-env I_MPI_DYNAMIC_CONNECTION=0 \
		osu_bw \
		-x 100 -i 1000 H H \
		>> $outdir/stdout_bandwidth_run$i.txt 2> $outdir/stderr_bandwidth_run$i.txt
done
