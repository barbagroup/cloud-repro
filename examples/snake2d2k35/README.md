# 2D flow around a snake cross-section (Re=2000, AoA=35deg)

All commands are run from the directory that contains the present README file.

To create the file containing the coordinates of the immersed boundary for the snake cross-section:

```bash
python scripts/create_body.py
```

Output: `snake2d35.body`.

To create the YAML node `mesh` (that contains information about the structured Cartesian grid):

```bash
python scripts/create_mesh_yaml.py
```

Output: `mesh.yaml` (content to be placed into the global YAML configuration file `config.yaml`).

To submit the simulation to Azure Batch:

```bash
shipard-driver
```

The Shell script will ask you to provide the path of the configuration directory for Batch Shipyard (which is `config_shipyard`) and your Microsoft Azure password.

To download locally the simulation data from Azure Storage:

```bash
az storage file download-batch --source myfileshare/snake2d2k35 --destination output --account-name <storage-account-name>
```

To plot the history of the force coefficients:

```bash
python scripts/plot_force_coefficients.py
```

To compute the vorticity field:

```bash
cd output
petibm-vorticity
```

To generate XDMF files to visualize the solution fields (with VisIt):

```bash
cd output
petibm-createxdmf
```

Outputs: `u.xmf`, `v.xmf`, `p.xmf`, and `wz.xmf`, all located in the sub-folder `output`.

The simulation was submitted to Azure Batch with Batch Shipyard to run in a pool of 2 compute nodes (NC24r) using 12 cores and 2 NVIDIA K80 GPU devices per node.
The size of the `output` folder downloaded from Azure Storage is `7.9 GB`.
The job computed 200,000 time steps (80 non-dimensional time units) in just over 7 hours.

```bash
conda create --name=py27-visit python=2.7
conda install --name=py27-visit numpy pathlib pyyaml
```

```bash
conda activate py27-cloud
export VISIT_DIR="<path/to/visit>"
python scripts/plot_wz_wake2d.py
conda deactivate
```
