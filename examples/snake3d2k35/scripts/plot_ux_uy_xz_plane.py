"""Plot the streamwise and cross-flow velocity components.

Plot the filled contours of the streamwise and cross-flow velocity components
at time-step 100000 (100 time units) in the x/z plane at y=-0.2.
"""

from matplotlib import pyplot, patches
import numpy
import pathlib
import yaml

import petibmpy


def interp_xzplane(y, u, y_target=0.0):
    """Perform linear interpolation of the 3D data at given y-location.

    Parameters
    ----------
    y : numpy.ndarray of floats
        The y-coordinates along a vertical gridline as a 1D array.
    u : numpy.ndarray of floats
        The 3D data.
    y_target : float (optional)
        The y-coordinate at which to interpolate the data.

    Returns
    -------
    u_target : numpy.ndarray of floats
        The 2D interpolated data.

    """
    idx = numpy.where(y >= y_target)[0][0]
    y0, y1 = y[idx - 1], y[idx]
    u0, u1 = u[:, idx - 1, :], u[:, idx, :]
    u_target = u0 + (y_target - y0) * (u1 - u0) / (y1 - y0)
    return u_target


# Get simulation directory and data directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Read the body file to add body location on the axes.
filepath = simudir / 'data' / 'snake2d.body'
with open(filepath, 'r') as infile:
    xb, _ = numpy.loadtxt(infile, skiprows=1, unpack=True)
xb_min, xb_max = numpy.min(xb), numpy.max(xb)

# Plot the filled contours of the velocity components in the x/z plane.
timestep = 100000  # time-step index
y_target = -0.2  # y-location where to interpolate
names = ['u', 'v']  # name of the velocity components to plot
pyplot.rc ('font', family='serif', size=16)
fig, ax = pyplot.subplots(figsize=(8.0, 4.0), nrows=len(names), sharex=True)
for i, name in enumerate(names):
    # Read the grid coordinates on which the velocity is located.
    gridpath = simudir / 'output' / 'grid.h5'
    x, y, z = petibmpy.read_grid_hdf5(gridpath, name)
    x_min, x_max = numpy.min(x), numpy.max(x)
    z_min, z_max = numpy.min(z), numpy.max(z)

    # Read the velocity data at prescribed time step.
    filepath = datadir / 'solution' / '{:0>7}.h5'.format(timestep)
    data = petibmpy.read_field_hdf5(filepath, name)

    # Perform linear interpolation.
    data_target = interp_xzplane(y, data, y_target=y_target)

    # Plot the filled contour, the 0-contour, and the body.
    ax[i].set_ylabel('z')
    levels = numpy.linspace(-1.0, 1.0, num=52)
    ax[i].contourf(*numpy.meshgrid(x, z), data_target,
                   levels=levels, cmap='viridis', extend='both')
    ax[i].contour(*numpy.meshgrid(x, z), data_target,
                  levels=[0.0], colors='black')
    ax[i].add_patch(patches.Rectangle((xb_min, z_min),
                                      xb_max - xb_min, z_max - z_min,
                                      color='grey', zorder=10))
    ax[i].axis('scaled', adjustable='box')
    ax[i].set_xlim(xb_min, x_max)
    ax[i].set_ylim(z_min, z_max)
ax[-1].set_xlabel('x')
fig.tight_layout()

# Save the figure as a PNG file.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'ux_uy_xz_plane.png'
fig.savefig(str(filepath), dpi=300, bbox_inches='tight')

pyplot.show()
