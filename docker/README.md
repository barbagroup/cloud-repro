# Docker images and Dockerfiles

The present directory contains the Dockfiles we used to build the Docker images to run benchmarks and simulations on Microsoft Azure with Azure Batch.

## Pull the Docker images from DockerHub

* OSU Micro-Benchmarks (version 5.6):

```bash
docker pull mesnardo/osubenchmarks:5.6-GPU-IntelMPI-ubuntu
```

* Poisson benchmarks with AmgXWrapper (version 1.4):

```bash
docker pull mesnardo/amgxwrapper:1.4-GPU-IntelMPI-ubuntu
```

* PetIBM (version 0.4):

```bash
docker pull barbagroup/petibm:0.4-GPU-IntelMPI-ubuntu
```

## Build the Docker images locally

The present directory contains three subfolders.
Each one has the Dockerfile we used to build the Docker images locally and run the benchmarks and simulations on Microsoft Azure:

* `osubenchmarks/Dockerfile`: point-to-point benchmark from OSU (version 5.6).
* `poisson/Dockerfile`: Poisson benchmarks with AmgXWrapper (version 1.4).
* `petibm/Dockerfile`: Flying-snake simulations with PetIBM (version 0.4).

**Note:** Only Intel MPI 5.x versions are compatible with the Azure Linux RDMA drivers.
We used the Intel MPI Library for Linux (2017, Update 2) to build the Docker images.
Upon [registration](https://software.seek.intel.com/performance-libraries), you will be able to download the product on the Intel Software website.
(The tarball should be named `l_mpi_2017.2.174.tgz` and be downloaded in the present directory.)

To build the Docker images on your local machine:

* OSU Micro-Benchmarks (version 5.6):

```bash
cd osubenchmarks
docker build --tag=osubenchmarks:5.6-GPU-IntelMPI-ubuntu -f Dockerfile .
```

* Poisson benchmarks with AmgXWrapper (version 1.4):

```bash
cd poisson
docker build --tag=amgxwrapper:1.4-GPU-IntelMPI-ubuntu -f Dockerfile .
```

* PetIBM (version 0.4):

```bash
cd petibm
docker build --tag=petibm:0.4-GPU-IntelMPI-ubuntu -f Dockerfile .
```

```bash
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
