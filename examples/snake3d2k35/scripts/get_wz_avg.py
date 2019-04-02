"""Average the spanwise vorticity field along the spanwise direction.

Write the 2D field values into HDF5 file.
"""

import pathlib
import numpy
import yaml

import petibmpy

name = 'wz'  # name of the field variable

# Get directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output' / 'solution'
outdir = simudir / 'output' / 'postprocessing' / (name + '_avg')
outdir.mkdir(parents=True, exist_ok=True)

# Read 3D grid and write 2D grid.
gridpath = simudir / 'output' / 'grid.h5'
x, y, _ = petibmpy.read_grid_hdf5(gridpath, name)
gridpath = outdir / 'grid.h5'
petibmpy.write_grid_hdf5(gridpath, name + '-avg', x, y)

# Get temporal parameters.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)['parameters']
dt = config['dt']
timesteps = [80000, 100000]

# Average the scalar field along the z-direction and write field.
for timestep in timesteps:
    print('[time step {}]'.format(timestep))
    filepath = datadir / '{:0>7}.h5'.format(timestep)
    data = petibmpy.read_field_hdf5(filepath, name)
    data_avg = numpy.mean(data, axis=0)
    filepath = outdir / '{:0>7}.h5'.format(timestep)
    petibmpy.write_field_hdf5(filepath, name + '-avg', data_avg)

# Write XDMF file to visualize field with VisIt.
filepath = outdir / (name + '-avg.xmf')
petibmpy.write_xdmf(filepath, outdir, gridpath, name + '-avg', dt,
                    states=timesteps)
