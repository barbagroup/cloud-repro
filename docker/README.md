# Docker images and Dockerfiles

The present directory contains four sub-folders:

* `osubenchmarks`
* `poisson`
* `petibm`
* `prepost`

The folder `prepost` contains the Dockerfile used to create the Docker image [`barbagroup/cloud-repro:latest`](https://cloud.docker.com/u/barbagroup/repository/docker/barbagroup/cloud-repro).
This image can be used to re-create a local computational environment with all the dependencies installed to perform pre-processing steps, submit jobs to Azure Batch through the command-line, and re-do the analysis to create the figures of the manuscript.

To pull the Docker image from DockerHub and create a container:

```shell
docker pull barbagroup/cloud-repro:latest
docker run -it barbagroup/cloud-repro:latest /bin/bash
```

Each of the three other sub-folders contains the Dockerfile we used to build the Docker images to run benchmarks and simulations on Microsoft Azure with Azure Batch.

**Important:** To be able to use the low-latency and high-bandwidth network of Azure with RMDA-capable nodes, we built the Docker images with the Intel MPI library for Linux (2017, Update 2). Please note that you must agree with the [Intel Simplified Software License](https://software.intel.com/en-us/license/intel-simplified-software-license) before using either of these Docker images.

The Docker image [`mesnardo/osubenchmarks:5.6-GPU-IntelMPI-ubuntu`](https://cloud.docker.com/u/mesnardo/repository/docker/mesnardo/osubenchmarks) is used to run the latency and bandwidth benchmarks from the [OSU Micro-Benchmarks](http://mvapich.cse.ohio-state.edu/benchmarks/) (version 5.6).
(Dockerfile in the sub-folder `osubenchmarks`.)

The Docker image [`mesnardo/amgxwrapper:1.4-GPU-IntelMPI-ubuntu`](https://cloud.docker.com/u/mesnardo/repository/docker/mesnardo/amgxwrapper) is used to run the Poisson benchmark from [AmgXWrapper](https://github.com/barbagroup/AmgXWrapper) (version 1.4).
(Dockerfile in the sub-folder `poisson`.)

The Docker image [`barbagroup/petibm:0.4-GPU-IntelMPI-ubuntu`](https://cloud.docker.com/u/barbagroup/repository/docker/barbagroup/petibm) is used to run the CFD simulations of the gliding snake models with [PetIBM](https://github.com/barbagroup/PetIBM) (version 0.4).
(Dockerfile in the sub-folder `petibm`.)

**Note:** Only Intel MPI 5.x versions are compatible with the Azure Linux RDMA drivers.
We used the Intel MPI Library for Linux (2017, Update 2) to build the Docker images.
Upon [registration](https://software.seek.intel.com/performance-libraries), you will be able to download the product on the Intel Software website.
(The tarball should be named `l_mpi_2017.2.174.tgz` and be downloaded in the present directory.)

To build the Docker images on your local machine (from the present directory):

* OSU Micro-Benchmarks (version 5.6):

```shell
docker build --tag=osubenchmarks:5.6-GPU-IntelMPI-ubuntu -f osubenchmarks/Dockerfile .
```

* Poisson benchmarks with AmgXWrapper (version 1.4):

```shell
docker build --tag=amgxwrapper:1.4-GPU-IntelMPI-ubuntu -f poisson/Dockerfile .
```

* PetIBM (version 0.4):

```shell
docker build --tag=petibm:0.4-GPU-IntelMPI-ubuntu -f petibm/Dockerfile .
```

* Computational environment for local pre- and post-processing steps:

```shell
cd prepost
docker build --tag=cloud-repro:latest -f Dockerfile .
```

```shell
$ docker version

Client:
 Version:           18.09.3
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        774a1f4
 Built:             Thu Feb 28 06:40:58 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.3
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.8
  Git commit:       774a1f4
  Built:            Thu Feb 28 05:59:55 2019
  OS/Arch:          linux/amd64
  Experimental:     false
```
