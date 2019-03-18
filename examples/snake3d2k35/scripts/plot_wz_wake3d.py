"""Create 3D contour figures of the z-component of the vorticity field."""

import os
import sys
import numpy
import pathlib

scriptdir = pathlib.Path(__file__).absolute().parents[3] / 'misc'
if scriptdir not in sys.path:
    sys.path.insert(0, str(scriptdir))
from visitplot import *


simudir = pathlib.Path(__file__).absolute().parents[1]
xdmfpath = simudir / 'output' / 'wz.xmf'
name = 'wz'
config_view = simudir / 'scripts' / 'visit_view3d.yaml'
bodypath = simudir / 'snake3d35.body'
p3dpath = simudir / 'output' / 'snake3d35.p3d'
figdir = simudir / 'figures'
prefix = 'wz_wake3d_'

# Create p3d file from body file.
with open(bodypath, 'r') as infile:
    x, y, z = numpy.loadtxt(infile, skiprows=1, unpack=True)
with open(p3dpath, 'wb') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y, z])

visit_plot_contour_3d(xdmfpath, name,
                      value_range=(-5.0, 5.0),
                      p3d_paths=[p3dpath],
                      config_view=config_view,
                      out_dir=figdir, out_prefix=prefix,
                      figsize=(1024, 1024),
                      visit_dir=os.environ.get('VISIT_DIR'))
