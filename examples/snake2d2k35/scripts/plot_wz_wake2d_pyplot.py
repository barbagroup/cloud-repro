"""Plot the 2D vorticity field at different time steps."""

import pathlib
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot
import numpy
import yaml

import petibmpy


name = 'wz'  # name of the field variable (z-vorticity)

# Get directories.
rootdir = pathlib.Path(__file__).absolute().parents[1]
datadir = rootdir / 'output'

# Read the grid.
gridpath = datadir / 'grid.h5'
x, y = petibmpy.read_grid_hdf5(gridpath, name)
X, Y = numpy.meshgrid(x, y)

# Read the body coordinates.
filepath = datadir / 'snake2d35.body'
with open(filepath, 'r') as infile:
    xb, yb = numpy.loadtxt(infile, skiprows=1, unpack=True)

# Read the time parameters from YAML configuration file.
filepath = rootdir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)['parameters']
nstart, nt, nsave = config['startStep'], config['nt'], config['nsave']
dt = config['dt']

# Select time units to plot.
times = [20.0, 44.0, 45.0, 80.0]
timesteps = [int(t / dt) for t in times]

# Plot the filled contour of the field variable at selected times.
pyplot.rc('font', family='serif', size=12)
fig, ax = pyplot.subplots(nrows=len(times), figsize=(5.0, 8.0), sharex=True)
levels = numpy.linspace(-5.0, 5.0, num=51)
for i, (time, timestep) in enumerate(zip(times, timesteps)):
    print('[time step {}]'.format(timestep))
    filepath = datadir / 'solution' / '{:0>7}.h5'.format(timestep)
    data = petibmpy.read_field_hdf5(filepath, name)
    ax[i].text(-0.5, 1.0, 't = {:.1f}'.format(time))
    ax[i].set_ylabel('y/c')
    ax[i].contourf(X, Y, data, levels=levels, extend='both')
    ax[i].plot(xb, yb, color='black')
    ax[i].axis('scaled', adjustable='box')
    ax[i].set_xlim(-1.0, 6.0)
    ax[i].set_ylim(-1.5, 1.5)
ax[-1].set_xlabel('x/c')
fig.tight_layout()

# Save the figure.
figdir = rootdir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'wz_multi_contourf.png'
fig.savefig(str(filepath), dpi=300, bbox_inches='tight')

pyplot.show()
