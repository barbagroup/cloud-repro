# Poisson benchmark on Microsoft Azure

We ran the Poisson benchmark from [AmgXWrapper](https://github.com/barbagroup/AmgXWrapper) (version 1.4) using H16r and NC24r instances of Microsoft Azure.
The Poisson benchmark was solved on CPU nodes (H16r instances) using the PETSc library, and on GPU nodes (NC24r) using the NVIDIA AmgX library.
We submitted jobs to Azure Batch on pools create with Batch Shipyard.
Each run was repeated 5 times.

## Contents

* `amgx`: input files to run the benchmark with NC24r instances.
* `petsc`: input files to run the benchmark with H16r instances.

## Run

Check the `README` file within each sub-folder.