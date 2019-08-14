# Poisson benchmarks on Colonial One

Colonial One is the HPC cluster at the George Washington University.
We ran the Poisson benchmark from [AmgXWrapper](https://github.com/barbagroup/AmgXWrapper) (version 1.4) using nodes from the `short` and `ivygpu` partitions on Colonial One.
The Poisson benchmark was solved on CPU nodes (`short`) using the PETSc library, and on GPU nodes (`ivygpu`) using the NVIDIA AmgX library.
Each run was repeated 5 times.

## Contents

* `amgx`: input files to run the Poisson benchmark on GPU nodes.
* `petsc`: input files to run the Poisson benchmark on CPU nodes.

## Run the benchmark

Copy (`scp` or `rsync`) the present folder to Colonial One.
Once you are on Colonial One, change directory to one of the case folders (e.g. `cd amgx/01_ivygpu`), modify the Shell script with the correct path to the AmgX library and to the AmgXWrapper library.
Then submit the job to the queue:

```bash
sbatch run-poisson.sh
```