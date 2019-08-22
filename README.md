# Reproducible workflow on a public cloud for computational fluid dynamics

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/barbagroup/cloud-repro/raw/master/LICENSE)
[![License](https://img.shields.io/badge/Zenodo-10.5281/zenodo.2642710-informational.svg)](https://doi.org/10.5281/zenodo.2642710)

* Olivier Mesnard (The George Washington University)
* Lorena A. Barba (The George Washington University)

Manuscript preprint on arXiv, submitted April 16, 2019: https://arxiv.org/abs/1904.07981

## Dependencies

* [Azure-CLI](https://github.com/Azure/azure-cli) (last used: `2.0.57`)
* [Batch Shipyard](https://github.com/Azure/batch-shipyard) (`3.6.1`)

Other dependencies for pre- and post-processing steps:

* [PetIBM](https://github.com/barbagroup/PetIBM) (`0.4`)
* [petibmpy](https://github.com/mesnardo/petibmpy) (`master`, commit `0f921da`, `0.1`)
* [VisIt](https://wci.llnl.gov/simulation/computer-codes/visit) (`2.12.3`)

We also provide a Docker image, [`barbagroup/cloud-repro:latest`](https://cloud.docker.com/u/barbagroup/repository/docker/barbagroup/cloud-repro), to create a container with the same computational environment for the pre- and post-processing steps.
See this [Dockerfile](https://github.com/barbagroup/cloud-repro/blob/master/docker/prepost/Dockerfile) to have the list of commands used to create the image.

To create a Docker container based on the `barbagroup/cloud-repro:latest` image:

```shell
docker pull barbagroup/cloud-repro:latest
docker run -it barbagroup/cloud-repro:latest /bin/bash
```

## LICENSE

**Not all content in this repository is open source.** The Python code for creating the figures is shared under a BSD 3-Clause License.
The written content in any Jupyter Notebooks is shared under a Creative Commons Attribution (CC-BY) license.
But please note that _the manuscript text is not open source;_ we reserve rights to the article content, which will be submitted for publication in a journal.
Only fair use applies in this case.
