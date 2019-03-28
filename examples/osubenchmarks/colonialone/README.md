# OSU Micro-Benchmarks on Colonial One

Colonial One is the HPC cluster at the George Washington University.
We ran the latency (`osu_latency`) and bandwidth (`osu_bw`) benchmarks of the [OSU Micro-Benchmarks](http://mvapich.cse.ohio-state.edu/benchmarks/) suite (version 5.6).
We used 2 nodes of the `ivygpu` queue (Dual 6-Core E5-2620v2 at 2.10 GHz) with FDR InfiniBand network.
Each benchmark was repeated 5 times.

## Contents

* `run-osu.sh`: script of the job to submit on Colonial One.

## Run the benchmarks

Once you ssh to Colonial One, modify the `run-osu.sh` to provide the location of the executables (i.e., modify the variable `bindir`).
Then submit the job to the queue:

```bash
sbatch run-osu.sh
```

## Output

The output files will be saved in the sub-folder `output`; it contains `stdout` and `stderr` files for each repeated run and each benchmark.
For example, the file `stdout_latency_run1.txt` contains the output of the latency benchmark for the second run.