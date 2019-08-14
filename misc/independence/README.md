# Grid-independence study

The present directory contains a Jupyter Notebook that compares the aerodynamic forces on the 3D snake cylinder for two different grids:

* a "coarse" grid with ~46 million cells,
* a "fine" grid with ~233 million cells.

The 3D flow around the snake cylinder at Reynolds number 2000 was computed on the two grids, and a comparison in the force coefficients was done to assess if the "coarse" grid would an acceptable candidate to run our exploratory analysis.

The simulation with the "coarse" grid ran on a single node (NC24r, Ubuntu-16.04).
The simulation on the "fine" grid ran in a Docker container on a cluster of 6 nodes (NC24r, CentOS-7.3 HPC) with Azure Batch and Batch Shipyard.

The Docker image used for the "fine"-grid simulation was built using the Dockerfile located in the sub-folder `docker`.
This image was published to a private repository on DockerHub as it uses the library NVIDIA AmgX-2.0 and the source code was not yet open source at the time we built it (shared with us under NDA).

The sub-folder `runs` contains the configuration and input files for the simulations reported in the Notebook.

The Jupyter Notebook is already executed, but if you want to re-run the cells, you will need to have the secondary data (such as the history of the forces).
These data along with the Notebook are deposited on [Zenodo](https://doi.org/10.5281/zenodo.2642711).
