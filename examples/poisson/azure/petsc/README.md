# Poisson benchmark on Microsoft Azure with H16r instances

We ran the Poisson benchmark from [AmgXWrapper](https://github.com/barbagroup/AmgXWrapper) (version 1.4) using H16r instances of Microsoft Azure.
The Poisson system is solved using a Conjugate-Gradient method from the PETSc library and a Classical Algebraic Multigrid preconditioner from Hypre BoomerAMG.

## Contents

* `01_h16r`: input files to solve on 1 H16r node.
* `02_h16r`: input files to solve on 2 H16r nodes.
* `04_h16r`: input files to solve on 4 H16r nodes.
* `08_h16r`: input files to solve on 8 H16r nodes.
* `config`: PETSc configuration file of the solver.

## Run

Make sure you have created a Azure Batch account and a Azure Storage account for your personal Azure subscription.
The environment variable `CLOUDREPRO` contains the path of the `cloud-repro` git folder on the local machine.

## Example: solve the Poisson system on a two-node pool

1- Change directory to folder `02_h16r`:

```shell
cd 02_h16r
```

2- Generate the YAML configuration with your credentials:

```shell
python $CLOUDREPRO/misc/generatecredentials.py \
    --resource-group <Name of the resource group> \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share> \
    --output config_shipyard/credentials.yaml
```

3- Create a symbolic link to the folder with the NVIDIA AmgX configuration file:

```shell
ln -s ../config config
```

4- Create the directory `poisson_petsc_002` in the fileshare on your Azure Storage account:

```shell
az storage directory create --name poisson_petsc_002 \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share>
```

IMPORTANT: for the run on a single-node pool (folder `01_h16r`), we do not ingress data to a GlusterFS volume to a Azure File Storage, thus, we need to upload the Shell script `run-poisson.sh` and the `config` folder to the fileshare on Azure Storage:

```shell
az storage file upload --source run-poisson.sh --path poisson_petsc_001 \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share>
az storage directory create --name poisson_petsc_001/config \
    --acount-name <Name of the storage account> \
    --share-name <Name of the file share>
az storage file upload --source config/poisson_solver.info --path poisson_petsc_001/config \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share>
```

5- Create the pool, ingress input files, submit the job, and delete the pool upon completion:

```shell
export SHIPYARD_CONFIGDIR=config_shipyard
shipyard pool add
shipyard data ingress
shipyard jobs add

## wait for task completion

shipyard jobs del
shipyard pool del
```

or, alternatively, you can use the Shell script `shipyard-driver` to automatically delete the pool once the task in the job completed successfully:

```shell
export PATH=$CLOUDREPRO/misc/bin:$PATH
shipyard-driver
```

The Shell script will ask you to provide the path of the configuration directory for Batch Shipyard (which is `config_shipyard` here) and your Microsoft Azure password.
By default, it will save the Batch Shipyard logging files into the sub-folder `log_shipyard`.

6- Download the output from Azure Storage to the local machine:

```shell
mkdir output
az storage file download-batch --destination output
    --source <Name of the file share>/poisson_petsc_002 \
    --account-name <Name of the storage account>
```

6- Delete the `poisson_petsc_002` directory on Azure Storage:

```shell
export PATH=$CLOUDREPRO/misc/bin:$PATH
az-storage-directory-delete --name poisson_petsc_002 \
    --account-name <Name of the storage account> \
    --share-name <Name of file share>
```