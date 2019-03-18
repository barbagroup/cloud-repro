"""Generate the coordinates of the snake boundary."""

import sys
import pathlib
import numpy
from matplotlib import pyplot

import petibmpy

# Read the original coordinates of the section.
rootdir = pathlib.Path(__file__).absolute().parents[1]
datadir = rootdir / 'data'
filepath = datadir / 'snake2d.body'
with open(filepath, 'r') as infile:
    x, y = numpy.loadtxt(infile, dtype=numpy.float64, skiprows=1, unpack=True)

# Apply rotation and regularize the geometry to desired resolution.
x, y = petibmpy.rotate2d(x, y, center=(0.0, 0.0), angle=-35.0)
x, y = petibmpy.regularize2d(x, y, ds=0.004)

# Write new coordinates in file located in simulation directory.
filepath = rootdir / 'snake2d35.body'
with open(filepath, 'w') as outfile:
    outfile.write(f'{x.size}\n')
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
