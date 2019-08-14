#!/usr/bin/env bash

#SBATCH --job-name="02petsc"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=short
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --time=00:20:00

n=2
ppn=16
np=$(($n * $ppn))

module load gcc/4.9.2
module load cuda/toolkit/8.0

source /c1/apps/intel-cluster-studio/2017.4/compilers_and_libraries_2017.4.196/linux/mpi/intel64/bin/mpivars.sh

AMGXWRAPPER_DIR="/groups/barbalab/software/amgxwrapper/1.4/linux-gnu-intelmpi-opt"
export PATH="$AMGXWRAPPER_DIR/example/poisson/bin":$PATH

AMGX_DIR="/groups/barbalab/software/amgx-2.0/linux-gnu-intelmpi-opt"
export LD_LIBRARY_PATH="$AMGX_DIR/lib":$LD_LIBRARY_PATH

configdir="../config"
outdir="output"
mkdir -p $outdir

niters=5
counter=1

while [ $counter -le $niters ]
do
	casename="poisson_petsc_${n}nodes_run${counter}"
	mpirun -np $np -ppn $ppn poisson \
		-caseName $casename \
		-mode PETSc \
		-cfgFileName $configdir/poisson_solver.info \
		-Nx 1000 -Ny 1000 -Nz 50 \
		-log_view ascii:${outdir}/view_run${counter}.log \
		-options_left > ${outdir}/stdout_run${counter}.txt 2> ${outdir}/stderr_run${counter}.txt
	((counter++))
done

exit 0
