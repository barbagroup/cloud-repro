#!/usr/bin/env bash
# Run OSU benchmark to evaluate point-to-point latency and bandwidth.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
outdir=$scriptdir

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

bindir="/opt/osu-micro-benchmarks/5.6/mpi/pt2pt"
export PATH=$bindir:$PATH

echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

cd $outdir

cp $AZ_BATCH_TASK_DIR/stdout.txt .
cp $AZ_BATCH_TASK_DIR/stderr.txt .

for i in `seq 1 5`; do
    mpirun -n 2 --ppn 1 --host $AZ_BATCH_HOST_LIST \
        -env I_MPI_FABRICS=dapl \
        -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 \
        -env I_MPI_DYNAMIC_CONNECTION=0 \
        osu_latency \
        -x 100 -i 10000 H H \
        >> $outdir/stdout_latency_run$i.txt 2> $outdir/stderr_latency_run$i.txt

    mpirun -n 2 --ppn 1 --host $AZ_BATCH_HOST_LIST \
        -env I_MPI_FABRICS=dapl \
        -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0 \
        -env I_MPI_DYNAMIC_CONNECTION=0 \
        osu_bw \
        -x 100 -i 1000 H H \
        >> $outdir/stdout_bandwidth_run$i.txt 2> $outdir/stderr_bandwidth_run$i.txt
done

exit 0