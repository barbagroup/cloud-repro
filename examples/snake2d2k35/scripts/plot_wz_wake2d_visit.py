"""Generate figures of the 2D pseudocolor of the 2D vorticity field."""

import numpy
import os
import pathlib
import sys

root_dir = pathlib.Path(__file__).absolute().parents[3]
scripts_dir = root_dir / 'misc'
if root_dir not in sys.path:
    sys.path.insert(0, str(scripts_dir))
from visitplot import *


simudir = pathlib.Path(__file__).absolute().parents[1]
xdmfpath = simudir / 'output' / 'postprocessing' / 'wz' / 'wz.xmf'
name = 'wz'
config_view = simudir / 'scripts' / 'visit_view2d.yaml'
body2dpath = simudir / 'output' / 'snake2d35.body'
curve2dpath = simudir / 'output' / 'snake2d35.curve'
figdir = simudir / 'figures'
prefix = 'wz_wake2d_'

# Create .curve file if not already present.
if not curve2dpath.is_file():
    with open(str(body2dpath), 'r') as infile:
        x, y = numpy.loadtxt(infile, skiprows=1, unpack=True)
    with open(str(curve2dpath), 'w') as outfile:
        numpy.savetxt(outfile, numpy.c_[x, y])

visit_plot_pseudocolor_2d(xdmfpath, name,
                          value_range=(-5.0, 5.0),
                          curve2d_paths=[curve2dpath],
                          config_view=config_view,
                          out_dir=figdir, out_prefix=prefix,
                          figsize=(1024, 1024),
                          visit_dir=os.environ.get('VISIT_DIR'), state=1)
