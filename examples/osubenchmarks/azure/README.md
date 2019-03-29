# OSU Micro-Benchmarks on Azure

We ran the latency (`osu_latency`) and bandwidth (`osu_bw`) benchmarks of the [OSU Micro-Benchmarks](http://mvapich.cse.ohio-state.edu/benchmarks) suite (version 5.6) on Microsoft Azure.
We used a pool of two NC24r instances (Dual 12-Core E5-2690v3 at 2.60 GHz) with FDR InfiniBand network.
Each benchmark was repeated 5 times.

## Contents

* `config_shipyard`: YAML configuration files for Batch Shipyard.
  * `config.yaml`: global configuration.
  * `pool.yaml`: pool configuration.
  * `jobs.yaml`: job configuration.
* `run-osu.sh`: Bash script to run inside the Docker container on Azure Batch.

(Note: the Batch Shipyard configuration file with the credentials, `credentials.yaml`, is not version-controlled as it contains sensitive information. You will have to generate it before creating the pool with Batch Shipyard.)

## Run

Make sure you have created a Azure Batch account and a Azure Storage account for your personal Azure subscription.
All command-lines written below are run from the `README`'s directory.
The environment variable `CLOUDREPRO` contains the path of the `cloud-repro` git folder on the local machine.

1- Generate the YAML configuration file with your credentials:

```shell
python $CLOUDREPRO/misc/generatecredentials.py \
    --resource-group <Name of the resource group> \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share> \
    --output config_shipyard/credentials.yaml
```

2- Create a `osubenchmarks` directory in the fileshare:

```shell
az storage directory create --name osubenchmarks \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share>
```

3- Upload the Bash script `run-osu.sh` to the storage account:

```shell
az storage file upload --source run-osu.sh --path osubenchmarks/run-osu.sh \
    --account-name <Name of the storage account> \
    --share-name <Name of the file share>
```

4- Create the pool, submit the job, and delete the pool upon completion:

```shell
export SHIPYARD_CONFIGDIR=config_shipyard
shipyard pool add
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

5- Download the output from Azure Storage to the local machine:

```shell
mkdir output
az storage file download-batch --destination output
    --source <Name of the file share>/osubenchmarks \
    --account-name <Name of the storage account>
```

6- Delete the `osubenchmarks` directory on Azure Storage:

```shell
export PATH=$CLOUDREPRO/misc/bin:$PATH
az-storage-directory-delete --name osubenchmarks \
    --account-name <Name of the storage account> \
    --share-name <Name of file share>
```

## Output

The output files will be saved in the sub-folder `output`; it contains `stdout` and `stderr` files for each repeated run and each benchmark.
For example, the file `stdout_latency_run1.txt` contains the output of the latency benchmark for the second run.