#!/bin/sh

#SBATCH --job-name="osu"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=ivygpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --time=01:00:00

module load gcc/4.9.2
module load cuda/toolkit/8.0
module load openmpi/1.8/gcc/4.9.2

bindir="/groups/barbalab/software/osu-micro-benchmarks/5.6/mpi/pt2pt"
export PATH=$bindir:$PATH

export CUDA_VISIBLE_DEVICES=0,1

# number of runs
nruns=5

outdir="output"
mkdir -p $outdir
cd $outdir

for (( i=0; i<$nruns; i++ ))
do
	echo "run $i"
			  BENCHMARK="5.3.2/mpi/pt2pt/osu_bw"
	time mpiexec -display-map -mca btl openib,self \
		osu_bw -d cuda -x 100 -i 1000 H H \
		> stdout_bandwidth_run$i.txt 2> stderr_bandwidth_run$i.txt
	time mpiexec -display-map -mca btl openib,self \
		osu_latency -d cuda -x 100 -i 1000 H H \
		> stdout_latency_run$i.txt 2> stderr_latency_run$i.txt
done
