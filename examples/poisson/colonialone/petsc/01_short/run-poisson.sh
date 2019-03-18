#!/usr/bin/env bash

#SBATCH --job-name="01petsc"
#SBATCH --output=log%j.out
#SBATCH --error=log%j.err
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=01:00:00

nodes=1

module load gcc/4.9.2
module load openmpi/1.8/gcc/4.9.2
module load cuda/toolkit/8.0

AMGXWRAPPER_DIR="/groups/barbalab/software/amgxwrapper/1.4/linux-openmpi-opt"
export PATH="$AMGXWRAPPER_DIR/example/poisson/bin":$PATH

AMGX_DIR="/groups/barbalab/software/amgx/git/master/linux-openmpi-opt"
export LD_LIBRARY_PATH="$AMGX_DIR/lib":$LD_LIBRARY_PATH

configdir="../config"
outdir="output"
mkdir -p $outdir

niters=5
counter=1

while [ $counter -le $niters ]
do
	casename="poisson_petsc_${nodes}nodes_run${counter}"
	mpiexec poisson \
		-caseName $casename \
		-mode PETSc \
		-cfgFileName $configdir/poisson_solver.info \
		-Nx 1000 -Ny 1000 -Nz 50 \
		-log_view ascii:${outdir}/view_run${counter}.log \
		-options_left >> ${outdir}/stdout_run${counter}.txt 2> ${outdir}/stderr_run${counter}.txt
	((counter++))
done

exit 0
